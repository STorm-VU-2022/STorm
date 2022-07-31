package storm.android

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.Html
import android.text.method.LinkMovementMethod
import storm.android.databinding.ActivityMainBinding
import storm.android.databinding.ActivityUploadBinding
import storm.android.databinding.ActivityUploadFileBinding
import storm.android.objects.MaterialCallback

class UploadFileActivity : AppCompatActivity() {
    private lateinit var binding : ActivityUploadFileBinding // UI element binding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUploadFileBinding.inflate(layoutInflater)
        binding.link.text = "http://193.219.91.103:5785/en/news/publication/${MaterialCallback.material.id}"
        setContentView(binding.root)
        binding.btnMenu.setOnClickListener {
            val intent = Intent(this, MainMenuActivity::class.java)
            startActivity(intent)
        }

    }
}