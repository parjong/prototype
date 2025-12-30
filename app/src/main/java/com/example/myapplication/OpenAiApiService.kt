package com.example.myapplication

import android.app.Service
import android.content.Intent
import android.os.IBinder
import androidx.localbroadcastmanager.content.LocalBroadcastManager
import io.ktor.serialization.kotlinx.json.*
import io.ktor.server.application.*
import io.ktor.server.cio.*
import io.ktor.server.engine.*
import io.ktor.server.plugins.contentnegotiation.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import kotlinx.serialization.Serializable

class OpenAiApiService : Service() {

    private lateinit var server: CIOApplicationEngine

    override fun onCreate() {
        super.onCreate()
        server = embeddedServer(CIO, port = 8080) {
            install(ContentNegotiation) {
                json()
            }
            routing {
                post("/v1/chat/completions") {
                    val payload = call.receiveText()
                    val intent = Intent("com.example.myapplication.REQUEST_PAYLOAD").apply {
                        putExtra("payload", payload)
                    }
                    LocalBroadcastManager.getInstance(this@OpenAiApiService).sendBroadcast(intent)

                    call.respond(ChatCompletionResponse(
                        id = "chatcmpl-123",
                        `object` = "chat.completion",
                        created = 1677652288,
                        model = "gpt-3.5-turbo-0125",
                        choices = listOf(
                            Choice(
                                index = 0,
                                message = Message(
                                    role = "assistant",
                                    content = "Hello! How can I help you today?"
                                ),
                                finish_reason = "stop"
                            )
                        ),
                        usage = Usage(
                            prompt_tokens = 9,
                            completion_tokens = 12,
                            total_tokens = 21
                        )
                    ))
                }
            }
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        server.start(wait = false)
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        server.stop(1_000, 2_000)
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}

@Serializable
data class ChatCompletionResponse(
    val id: String,
    val `object`: String,
    val created: Long,
    val model: String,
    val choices: List<Choice>,
    val usage: Usage
)

@Serializable
data class Choice(
    val index: Int,
    val message: Message,
    val finish_reason: String
)

@Serializable
data class Message(
    val role: String,
    val content: String
)

@Serializable
data class Usage(
    val prompt_tokens: Int,
    val completion_tokens: Int,
    val total_tokens: Int
)