import asyncio
import logging
import os
from contextlib import contextmanager
from datetime import timedelta
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from sqlmodel import Session, select

from ..db.constants import MatchType
from ..db.manager import DBManager
from ..db.models import ModelAlias, ModelVariant, Thread
from ..db.store import Store
from ..engine.github import GitHubClient
from ..engine.sync import SyncEngine

console = Console()
logging.getLogger("httpx").setLevel(logging.WARNING)


@contextmanager
def get_store():
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")
    manager = DBManager(db_path)
    manager.initialize()
    store = Store(manager.get_engine())
    try:
        yield store
    finally:
        pass


@click.group()
def cli():
    """Octopith: GitHub Semantic Knowledge Base Tool"""
    pass


@cli.command()
@click.argument("repo_urls", nargs=-1)
@click.option("--duration", help="Duration to sync (e.g., 30m, 1h)")
def sync(repo_urls, duration):
    """Sync repositories data."""
    token = os.getenv("OCTOPITH_GITHUB_TOKEN")
    if not token:
        console.print("[red]Error: OCTOPITH_GITHUB_TOKEN environment variable is not set.[/red]")
        return

    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")

    manager = DBManager(db_path)
    manager.initialize()
    store = Store(manager.get_engine())
    gh_client = GitHubClient(token)
    engine = SyncEngine(store, gh_client)

    # Convert duration to seconds
    seconds = None
    if duration:
        if duration.endswith("m"):
            seconds = int(duration[:-1]) * 60
        elif duration.endswith("h"):
            seconds = int(duration[:-1]) * 3600
        elif duration.endswith("s"):
            seconds = int(duration[:-1])
        else:
            seconds = int(duration)

    async def run_sync():
        if not repo_urls:
            # Sync all registered repos
            repos = store.list_repositories()
            for repo in repos:
                console.print(f"Syncing [blue]{repo.full_name}[/blue]...")
                await engine.sync_repository(repo.api_url, duration_seconds=seconds)
        else:
            for url in repo_urls:
                console.print(f"Syncing [blue]{url}[/blue]...")
                await engine.sync_repository(url, duration_seconds=seconds)

    asyncio.run(run_sync())
    console.print("[green]Sync completed.[/green]")


@cli.command(help=MatchType.get_all_descriptions())
@click.argument("query")
@click.option("--fast", is_flag=True, help="Use keyword search only (FTS)")
@click.option("--rich", is_flag=True, help="Output results in Rich Table format")
@click.option("--repo", "repo_names", multiple=True, help="Filter by repository name")
@click.option("--limit", default=10, type=int, help="Limit number of results (default: 10)")
def search(query, fast, rich, repo_names, limit):
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")

    if not db_path.exists():
        console.print(f"[red]Error: Database file not found at {db_path}[/red]")
        return

    manager = DBManager(db_path)
    manager.initialize()
    store = Store(manager.get_engine())

    repo_ids = []
    if repo_names:
        for name in repo_names:
            repo = store.get_repository_by_name(name)
            if repo:
                repo_ids.append(repo.id)
            else:
                console.print(f"[yellow]Warning: Repository {name} not found in database.[/yellow]")

    if fast:
        results = store.search_fast(query, repo_ids=repo_ids if repo_ids else None, limit=limit)
    else:
        # Try Hybrid Search
        embed_variant = store.get_model_variant_by_alias("nomic-embed-text")
        if not embed_variant:
            console.print(
                "[yellow]Warning: No default embedding model found. Falling back to fast search.[/yellow]"
            )
            results = store.search_fast(query, repo_ids=repo_ids if repo_ids else None, limit=limit)
        else:
            import asyncio

            from octopith.engine.inference import OllamaAdapter

            adapter = OllamaAdapter(model_name=embed_variant.model_name)
            try:
                query_vector = asyncio.run(adapter.embed(query))
                results = store.search_hybrid(
                    query, query_vector, repo_ids=repo_ids if repo_ids else None, limit=limit
                )
            except Exception as e:
                console.print(
                    f"[red]Error during semantic search: {e}. Falling back to fast search.[/red]"
                )
                results = store.search_fast(
                    query, repo_ids=repo_ids if repo_ids else None, limit=limit
                )

    if not results:
        if rich:
            console.print("No results found.")
        else:
            import json

            print(json.dumps([]))
        return

    if not rich:
        import json

        # Include repo full_name and identifier in JSON results
        json_results = []
        for res in results:
            repo = store.get_repository(res["repo_id"])
            full_name = repo.full_name if repo else "Unknown"
            res["repo_full_name"] = full_name
            res["identifier"] = f"{full_name}#{res.get('number', 'N/A')}"
            json_results.append(res)
        print(json.dumps(json_results, indent=2, ensure_ascii=False))
        return

    table = Table(title=f"Search Results for: {query}")
    table.add_column("Identifier", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Match", style="blue")
    table.add_column("Title", style="green")
    table.add_column("Author", style="yellow")
    table.add_column("Updated At", style="dim")
    if not fast:
        table.add_column("Score", justify="right", style="bold white")

    for res in results:
        repo = store.get_repository(res["repo_id"])
        full_name = repo.full_name if repo else "Unknown"
        identifier = f"{full_name}#{res.get('number', 'N/A')}"
        row = [
            identifier,
            res["type"],
            res.get("match_label", "Unknown"),
            res["title"],
            res["author"] or "N/A",
            res["last_known_updated_at"],
        ]
        if not fast:
            row.append(f"{res.get('score', 0.0):.4f}")
        table.add_row(*row)

    console.print(table)


def parse_duration(duration_str: str) -> float:
    """Parse duration strings like '10s', '5m', '1h' into seconds."""
    if not duration_str:
        return 0
    unit = duration_str[-1].lower()
    val = float(duration_str[:-1])
    if unit == "s":
        return val
    if unit == "m":
        return val * 60
    if unit == "h":
        return val * 3600
    return val


# Model Management Helpers
def manage_model_use(model_name: str, alias: str, model_type: str):
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")
    manager = DBManager(db_path)

    engine_name = "ollama"
    tag = "default"
    full_name = model_name
    if "#" in full_name:
        full_name, tag = full_name.split("#", 1)

    real_model = full_name
    if "/" in full_name:
        engine_name, real_model = full_name.split("/", 1)

    with Session(manager.get_engine()) as session:
        variant = session.exec(
            select(ModelVariant).where(
                ModelVariant.engine == engine_name,
                ModelVariant.model_name == real_model,
                ModelVariant.variant_tag == tag,
                ModelVariant.type == model_type,
            )
        ).first()

        if not variant:
            if engine_name == "ollama":
                import httpx

                try:
                    resp = httpx.post("http://127.0.0.1:11434/api/show", json={"name": real_model})
                    if resp.status_code != 200:
                        console.print(
                            f"[red]Error: Model '{real_model}' not found in Ollama.[/red]"
                        )
                        return
                except Exception as e:
                    console.print(f"[red]Error connecting to Ollama: {e}[/red]")
                    return

            import json

            variant = ModelVariant(
                engine=engine_name,
                model_name=real_model,
                variant_tag=tag,
                type=model_type,
                config_data=json.dumps({"temperature": 0.1}),
            )
            session.add(variant)
            session.commit()
            session.refresh(variant)
            console.print(
                f"[green]Registered new {model_type} variant: {engine_name}/{real_model}#{tag}[/green]"
            )

        # 1. Register the requested alias (or the model name itself if alias is None)
        target_alias = alias if alias else full_name
        existing_alias = session.get(ModelAlias, target_alias)
        if existing_alias:
            existing_alias.variant_id = variant.id
            session.add(existing_alias)
        else:
            new_alias = ModelAlias(id=target_alias, variant_id=variant.id)
            session.add(new_alias)

        # 2. DESIGN.md: If no 'default' alias exists for this type, set this one as default automatically
        has_default = session.exec(
            select(ModelAlias)
            .join(ModelVariant)
            .where(ModelVariant.type == model_type, ModelAlias.id == "default")
        ).first()

        if not has_default:
            default_alias = ModelAlias(id="default", variant_id=variant.id)
            session.add(default_alias)
            console.print(
                f"[blue]Note: No default {model_type} model was set. '{target_alias}' is now the default.[/blue]"
            )

        session.commit()
        console.print(
            f"[green]Alias '{target_alias}' now points to {engine_name}/{real_model}#{tag}[/green]"
        )


def manage_model_list(model_type: str, title: str):
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")
    manager = DBManager(db_path)

    with Session(manager.get_engine()) as session:
        variants = session.exec(select(ModelVariant).where(ModelVariant.type == model_type)).all()
        aliases = session.exec(select(ModelAlias)).all()
        variant_to_aliases = {}
        for a in aliases:
            variant_to_aliases.setdefault(a.variant_id, []).append(a.id)

        from rich.table import Table

        table = Table(title=title)
        table.add_column("Source (Engine/Model#Tag)", style="green")
        table.add_column("Default", justify="center", style="bold yellow")
        table.add_column("Other Aliases", style="cyan")

        for v in variants:
            tag = v.variant_tag if v.variant_tag else "default"
            source = f"{v.engine}/{v.model_name}#{tag}"
            v_aliases = variant_to_aliases.get(v.id, [])
            is_default = "Yes" if "default" in v_aliases else ""
            other_aliases = ", ".join([a for a in v_aliases if a != "default"])
            table.add_row(source, is_default, other_aliases)

        console.print(table)


@cli.command(
    help="Summarize threads and build intelligence. Automatically runs embedding unless --no-embed is set."
)
@click.option("--repo", help="Specific repository full name to process (e.g., owner/repo)")
@click.option("--duration", help="Time limit for processing (e.g., 30m, 1h)")
@click.option("--model", default="default", help="Summary model alias to use")
@click.option("--embed-model", default="default", help="Embedding model alias to use")
@click.option("--no-embed", is_flag=True, help="Skip embedding process")
def digest(duration, repo, model, embed_model, no_embed):
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")
    manager = DBManager(db_path)
    # Ensure tables exist (handles migration to v1.1.0)
    manager.initialize()

    store = Store(manager.get_engine())
    store.ensure_summary_types()

    # 1. Summarization Phase
    summary_variant = store.get_model_variant_by_alias(model)
    if not summary_variant:
        console.print(f"[red]Error: Summary model alias '{model}' not found.[/red]")
        return

    repo_id = None
    if repo:
        repo_obj = store.get_repository_by_name(repo)
        if not repo_obj:
            console.print(f"[red]Repository not found: {repo}[/red]")
            return
        repo_id = repo_obj.id

    from octopith.engine.digest import DigestEngine
    from octopith.engine.inference import OllamaAdapter
    from octopith.engine.summarizer import Summarizer

    summary_adapter = OllamaAdapter(model_name=summary_variant.model_name)
    summarizer = Summarizer(summary_adapter)
    engine = DigestEngine(store, summarizer)
    duration_secs = parse_duration(duration) if duration else None

    import asyncio

    console.print(f"[green]Starting summarization using: {summary_variant.model_name}...[/green]")
    asyncio.run(engine.run(duration_seconds=duration_secs, model_alias=model, repo_id=repo_id))

    # 2. Embedding Phase (Default)
    if not no_embed:
        actual_embed_alias = "nomic-embed-text" if embed_model == "default" else embed_model
        embed_variant = store.get_model_variant_by_alias(actual_embed_alias)
        if not embed_variant:
            # If no embedding model is configured yet, we might want to warn but not fail the whole digest
            console.print(
                f"[yellow]Warning: Embedding model alias '{embed_model}' not found. Skipping auto-embed.[/yellow]"
            )
            console.print(
                "[yellow]Use 'embedding-model use <model>' to set a default embedding model.[/yellow]"
            )
            return

        from octopith.engine.embedding import EmbeddingEngine

        embed_adapter = OllamaAdapter(model_name=embed_variant.model_name)
        emb_engine = EmbeddingEngine(store, embed_adapter)

        # Calculate remaining time for embedding if duration was set
        # For simplicity, we'll give embedding its own small window or full remaining time
        # Here we just run it.
        console.print(
            f"[green]Starting auto-embedding using: {embed_variant.model_name}...[/green]"
        )
        asyncio.run(emb_engine.run())


@cli.command(help="Manually generate embeddings for search.")
@click.option("--duration", help="Time limit for embedding (e.g., 30m, 1h)")
@click.option("--model", default="default", help="Embedding model alias to use")
def embed(duration, model):
    config_dir = Path(os.getenv("OCTOPITH_CONFIG_DIR", "~/.config/octopith")).expanduser()
    db_path = config_dir / os.getenv("OCTOPITH_DB_PATH", "octopith.sqlite")
    manager = DBManager(db_path)
    store = Store(manager.get_engine())

    model_variant = store.get_model_variant_by_alias(model)
    if not model_variant:
        console.print(f"[red]Error: Model alias '{model}' not found.[/red]")
        return

    from octopith.engine.embedding import EmbeddingEngine
    from octopith.engine.inference import OllamaAdapter

    adapter = OllamaAdapter(model_name=model_variant.model_name)
    engine = EmbeddingEngine(store, adapter)
    duration_secs = parse_duration(duration) if duration else None
    td = timedelta(seconds=duration_secs) if duration_secs else None

    import asyncio

    console.print(f"[green]Starting embedding using model: {model_variant.model_name}...[/green]")
    asyncio.run(engine.run(duration=td))


@cli.group(name="thread", help="Inspect individual threads/issues.")
def thread():
    """Inspect individual threads and discussions."""
    pass


@thread.command(name="show", help="Show details and summary of a specific thread.")
@click.argument("identifier")
@click.option("--json", "as_json", is_flag=True, help="Output in JSON format")
def thread_show(identifier, as_json):
    """Show details and AI summary of a specific thread (e.g., owner/repo#number)."""
    import json as json_mod

    from rich.markdown import Markdown
    from rich.panel import Panel

    # Parse identifier: owner/repo#number
    try:
        if "#" not in identifier:
            raise ValueError("Identifier must be in format 'owner/repo#number'")
        full_name, number_str = identifier.split("#")
        number = int(number_str)
    except Exception as e:
        console.print(f"[red]Error parsing identifier: {e}[/red]")
        return

    with get_store() as store:
        repo = store.get_repository_by_name(full_name)
        if not repo:
            console.print(f"[red]Repository not found: {full_name}[/red]")
            return

        with Session(store.engine) as session:
            statement = select(Thread).where(Thread.repo_id == repo.id, Thread.number == number)
            thread_obj = session.exec(statement).first()

        if not thread_obj:
            console.print(f"[red]Thread not found: {identifier}[/red]")
            return

        summary = store.get_thread_summary(thread_obj.id)

        if as_json:
            result = {
                "identifier": identifier,
                "title": thread_obj.title,
                "author": thread_obj.author,
                "url": thread_obj.url,
                "summary": summary.content if summary else None,
                "last_updated_at": thread_obj.last_known_updated_at.isoformat()
                if hasattr(thread_obj.last_known_updated_at, "isoformat")
                else thread_obj.last_known_updated_at,
            }
            print(json_mod.dumps(result, indent=2, ensure_ascii=False))
            return

        # Rich output
        console.print(f"[bold cyan]Thread:[/bold cyan] {identifier}")
        console.print(f"[bold]Title:[/bold] {thread_obj.title}")
        console.print(f"[bold]Author:[/bold] {thread_obj.author}")
        console.print(f"[bold]URL:[/bold] {thread_obj.url}")
        console.print("-" * 40)

        if summary:
            console.print(
                Panel(Markdown(summary.content), title="AI Summary", border_style="green")
            )
        else:
            console.print(
                "[yellow]No AI summary found for this thread. Run 'octopith digest' to generate one.[/yellow]"
            )


@cli.group(name="summary-model", help="Manage models used for summarization.")
def summary_model():
    pass


@summary_model.command(name="use", help="Set a summary model variant to an alias.")
@click.argument("model_name")
@click.option("--alias", help="Alias to set")
def summary_model_use(model_name, alias):
    manage_model_use(model_name, alias, "summary")


@summary_model.command(name="list", help="List all summary model variants.")
def summary_model_list():
    manage_model_list("summary", "Summary Model Variants")


@cli.group(name="embedding-model", help="Manage models used for embedding.")
def embedding_model():
    pass


@embedding_model.command(name="use", help="Set an embedding model variant to an alias.")
@click.argument("model_name")
@click.option("--alias", help="Alias to set")
def embedding_model_use(model_name, alias):
    manage_model_use(model_name, alias, "embedding")


@embedding_model.command(name="list", help="List all embedding model variants.")
def embedding_model_list():
    manage_model_list("embedding", "Embedding Model Variants")


if __name__ == "__main__":
    cli()
