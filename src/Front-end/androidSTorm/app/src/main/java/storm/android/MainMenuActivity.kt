package storm.android

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import storm.android.databinding.ActivityMainMenuBinding
import java.io.File
import android.os.Environment
import android.util.Log
import androidx.core.app.ActivityCompat
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import storm.android.network.ApiClient
import storm.android.network.SubjectModel
import storm.android.objects.SubjectObject


class MainMenuActivity : AppCompatActivity() {
    private lateinit var binding : ActivityMainMenuBinding // UI element binding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainMenuBinding.inflate(layoutInflater)
        getSubjects()
        setContentView(binding.root)
        binding.button.setOnClickListener{
            val intent = Intent(this, UploadActivity::class.java)
            val storage = isStoragePermissionGranted()
            startActivity(intent)
        }
    }
    fun isStoragePermissionGranted(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_GRANTED && checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_GRANTED && checkSelfPermission(Manifest.permission.MANAGE_EXTERNAL_STORAGE)
                == PackageManager.PERMISSION_GRANTED
            ) {
                Log.v("TAG", "Permission is granted")
                true
            } else {
                Log.v("TAG", "Permission is revoked")
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE),
                    1
                )
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE),
                    1
                )
                ActivityCompat.requestPermissions(
                    this,
                    arrayOf(Manifest.permission.MANAGE_EXTERNAL_STORAGE),
                    1
                )
                false
            }
        } else { //permission is automatically granted on sdk<23 upon installation
            Log.v("TAG", "Permission is granted")
            true
        }
    }

    private fun getSubjects() {
        val client = ApiClient.apiService.getSubjects()
        client.enqueue(object : Callback<MutableList<SubjectModel>> {
            override fun onResponse(call: Call<MutableList<SubjectModel>>, response: Response<MutableList<SubjectModel>>) {
                if(response.isSuccessful){
                    Log.d("TestCategories! ", ""+ response.body())
                    SubjectObject.subjects = response.body()!!
                    Log.d("TestCategoryBody! ", ""+ SubjectObject.subjects)
                }
            }
            override fun onFailure(call: Call<MutableList<SubjectModel>>, response: Throwable) {
                Log.e("Something went wrong! ", ""+response.message)
            }
        })
    }
}