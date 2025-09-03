import pkgutil
import importlib

def import_submodules(package_name):
    """
    Recursively imports all submodules of a given package.

    Args:
        package_name (str): The name of the package to import submodules from.

    Returns:
        dict: A dictionary where keys are fully qualified module names and
              values are the imported module objects.
    """
    results = {}
    package = importlib.import_module(package_name)
    
    # Iterate through all modules and subpackages within the given package's path
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__, package_name + '.'):
        full_name = name
        try:
            # Import the module and store it in the results dictionary
            module = importlib.import_module(full_name)
            results[full_name] = module
            
            # If it's a subpackage, recursively call the function
            if is_pkg:
                results.update(import_submodules(full_name))
        except ImportError as e:
            print(f"Could not import module {full_name}: {e}")
    return results

imported_modules = import_submodules('my')
print(imported_modules.keys())

from my.X import K as REGISTERED_CLS

print('Create an object from 1st class')
obj = REGISTERED_CLS[0]()

