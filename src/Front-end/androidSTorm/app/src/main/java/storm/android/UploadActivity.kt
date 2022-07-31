package storm.android

import android.Manifest
import android.R
import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Environment
import android.os.FileUtils
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.core.app.ActivityCompat
import net.lingala.zip4j.ZipFile
import okhttp3.MediaType
import okhttp3.MultipartBody
import okhttp3.RequestBody
import okhttp3.ResponseBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import storm.android.databinding.ActivityUploadBinding
import storm.android.helper.RealPathUtils
import storm.android.helper.Zip
import storm.android.network.ApiClient
import storm.android.network.ApiServices
import storm.android.network.MaterialTakeModel
import storm.android.objects.*
import java.io.BufferedInputStream
import java.io.File
import java.io.FileInputStream
import java.io.InputStream
import java.nio.file.Files
import java.util.zip.ZipInputStream
import android.widget.ArrayAdapter
import android.widget.Spinner

class UploadActivity : AppCompatActivity() {
    private lateinit var binding : ActivityUploadBinding // UI element binding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityUploadBinding.inflate(layoutInflater)
        spinnerAdapter()
        setContentView(binding.root)

        binding.btnCont.setOnClickListener {
            MaterialUpObject.material.description = binding.editDesc.text.toString()
            MaterialUpObject.material.title = binding.editTitle.text.toString()
            MaterialUpObject.material.short_description = binding.editDesc.text.toString()
            MaterialUpObject.material.is_public = "True"
            MaterialUpObject.material.student_year = (binding.spinnerGrades.selectedItem.toString()).toInt()
            MaterialUpObject.material.subject = SubjectObject.subjects!!.find{ it.name == binding.spinnerSubjects.selectedItem.toString()}!!.id
            MaterialUpObject.material.language = binding.spinnerLangs.selectedItem.toString()
            postMaterialInfo()
            var granted = isStoragePermissionGranted()

            openGalleryForImages()
        }
    }

    private fun spinnerAdapter(){
        val adapter: ArrayAdapter<String> = ArrayAdapter<String>(
            this,
            R.layout.simple_spinner_item
        )

        adapter.setDropDownViewResource(R.layout.simple_spinner_dropdown_item)
        binding.spinnerSubjects.adapter = adapter

        for(subject in SubjectObject.subjects!!){
            adapter.add(subject.name)
        }
    }

    private fun postMaterialInfo() {
        println(MaterialUpObject.material)
        val clientPOST = ApiClient.apiService.pushPostMaterial(MaterialUpObject.material, "Bearer " + JwtObject.userJwt.access)
        Log.d("callNetworkPOST", "has been called")
        clientPOST.enqueue(object : Callback<MaterialTakeModel> {
            override fun onResponse(call: Call<MaterialTakeModel>, response: Response<MaterialTakeModel>) {
                if(response.isSuccessful){
                    Log.d("TEST", ""+ response.body())
                    MaterialCallback.material = response.body()!!
                }
                else {
                    Log.d("TESTfail", "" + response.code() + MaterialUpObject.material + JwtObject.userJwt.access)
                }
            }
            override fun onFailure(call: Call<MaterialTakeModel>, response: Throwable) {
                Log.e("TESTFail ", ""+response.message)
            }
        })
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

    val REQUEST_CODE = 200

    private fun openGalleryForImages() {

        // For latest versions API LEVEL 19+
        var intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
        intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
        intent.addCategory(Intent.CATEGORY_OPENABLE)
        intent.type = "image/*"
        startActivityForResult(intent, REQUEST_CODE)

    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (resultCode == Activity.RESULT_OK && requestCode == REQUEST_CODE){
            // if multiple images are selected
            if (data?.clipData != null) {
                var count = data.clipData!!.itemCount
                Log.v("TAG", "1 " + data.clipData!!.itemCount)
                for (i in 0 until count) {
                    var imageUri: Uri? = data.clipData!!.getItemAt(i).uri
                    Uris.ourUris?.add(imageUri)
                    Log.d("image", "" + imageUri)
                    ZipFile(Environment.getExternalStorageDirectory().toString() + "/android_upload.zip").addFile(File(RealPathUtils.getRealPathFromURI_API19(this, imageUri)))
                    postFile2()
                }

            } else if (data?.data != null) {
                var imageUri: Uri = data.data!!
                File(imageUri.path)
                Log.d("image", "" + imageUri)
                Uris.ourUri = imageUri
                postFile()

            }
        }
    }

    private fun postFile() {
        var path = RealPathUtils.getRealPathFromURI_API19(this, Uris.ourUri);

        val file = File(path)

        val targetStream: InputStream = FileInputStream(file)

        val body = RequestBody.create(MediaType.parse("application/octet"), targetStream.readBytes())

        val req: Call<ResponseBody?>? = ApiClient.apiService.postImage("http://193.219.91.103:5785/restapi/publication/${MaterialCallback.material.id}/${(path.substring(path.lastIndexOf("/")+1))}/", body, "Bearer " + JwtObject.userJwt.access)
        req!!.enqueue(object : Callback<ResponseBody?> {
            override fun onResponse(call: Call<ResponseBody?>, response: Response<ResponseBody?>) {
                // Do Something
                Log.d("TESTPUTSuccess", ""+ response.body())
            }

            override fun onFailure(call: Call<ResponseBody?>, t: Throwable) {
                t.printStackTrace()
                Log.d("TESTPUT", "failed")
            }
        })
        val intent = Intent(this, UploadFileActivity::class.java)
        startActivity(intent)

    }



private fun postFile2() {
    val file = File(Environment.getExternalStorageDirectory().toString() + "/android_upload.zip")
    val ba = Files.readAllBytes(file.toPath())

    val body = RequestBody.create(MediaType.parse("application/zip"), ba)
    Log.d("TESTPUTSuccess", ""+ "http://193.219.91.103:5785/restapi/publication/${MaterialCallback.material.id}/android_upload.zip")

    val req: Call<ResponseBody?>? = ApiClient.apiService.postImage("http://193.219.91.103:5785/restapi/publication/${MaterialCallback.material.id}/zip.zip/", body, "Bearer " + JwtObject.userJwt.access)
    req!!.enqueue(object : Callback<ResponseBody?> {
        override fun onResponse(call: Call<ResponseBody?>, response: Response<ResponseBody?>) {
            Log.d("TESTPUTSuccess", ""+ response.message() + response.code())
        }

        override fun onFailure(call: Call<ResponseBody?>, t: Throwable) {
            t.printStackTrace()
            Log.d("TESTPUT", "failed")
        }
    })
    val intent = Intent(this, UploadFileActivity::class.java)
    startActivity(intent)

}
}