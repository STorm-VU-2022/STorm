package storm.android

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View.SYSTEM_UI_FLAG_FULLSCREEN
import android.widget.Toast
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import storm.android.databinding.ActivityMainBinding
import storm.android.network.ApiClient
import storm.android.network.JwtModel
import storm.android.network.NetworkChecker.isNetworkAvailable
import storm.android.objects.DummyObject
import storm.android.objects.JwtObject
import storm.android.objects.UserObject
import storm.android.user.Dummy

class MainActivity : AppCompatActivity() {

    private lateinit var binding : ActivityMainBinding // UI element binding
    override fun onCreate(savedInstanceState: Bundle?) {
    super.onCreate(savedInstanceState)
    binding = ActivityMainBinding.inflate(layoutInflater)
    setContentView(binding.root)
    window.decorView.systemUiVisibility = SYSTEM_UI_FLAG_FULLSCREEN
    val networkOnline = isNetworkAvailable(this)
    //Displays a little pop up at the bottom of the screen (and goes to the question activity)
    binding.btnMenu.setOnClickListener {
        if(networkOnline){
            when {
                binding.username.text.toString().isEmpty() -> {
                    Toast.makeText(this@MainActivity, getString(R.string.main_activity_no_username_selected_toast), Toast.LENGTH_SHORT).show()
                }
                binding.password.text.toString().isEmpty() -> {
                    Toast.makeText(this@MainActivity, getString(R.string.main_activity_no_password_selected_toast), Toast.LENGTH_SHORT).show()
                }
                else -> {
                    UserObject.currentUser.email = binding.username.text.toString()
                    UserObject.currentUser.password = binding.password.text.toString()
                    callNetworkLogin()
                    Thread.sleep(100)
                }
            }
        }
        else{
            Toast.makeText(this@MainActivity, getString(R.string.no_internet), Toast.LENGTH_LONG).show()
        }
    }
}

private fun callNetworkLogin() {
    val intent = Intent(this, MainMenuActivity::class.java)
    val clientPOST = ApiClient.apiService.pushPostLogin(UserObject.currentUser)
    Log.d("callNetworkPOST", "has been called")
    clientPOST.enqueue(object : Callback<JwtModel> {
        override fun onResponse(call: Call<JwtModel>, response: Response<JwtModel>) {
            if(response.isSuccessful){
                Log.d("TEST", ""+ response.body())
                JwtObject.userJwt = response.body()!!
                Log.d("TEST", ""+ JwtObject.userJwt)
                Toast.makeText(this@MainActivity, getString(R.string.main_activity_welcome_overloaded_toast,binding.username.text.toString()), Toast.LENGTH_SHORT).show()
                startActivity(intent)
            }
            else {
                Log.d("TESTfail", "" + response.code())
                Toast.makeText(this@MainActivity, getString(R.string.main_activity_login_details_incorrect_toast), Toast.LENGTH_SHORT).show()
            }
        }
        override fun onFailure(call: Call<JwtModel>, response: Throwable) {
            Log.e("TESTFail ", ""+response.message)
        }
    })

}
}