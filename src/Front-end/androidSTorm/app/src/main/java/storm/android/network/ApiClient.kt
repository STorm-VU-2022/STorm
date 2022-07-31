package storm.android.network

import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import retrofit2.Call
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import retrofit2.http.*
import storm.android.user.UserModel
import okhttp3.RequestBody

import okhttp3.ResponseBody

import retrofit2.http.POST


object ApiClient {
    private const val BASE_URL = "http://193.219.91.103:5785"

    private val moshi = Moshi.Builder().add(KotlinJsonAdapterFactory()).build()

    // Retrofit client instance
    private val retrofit : Retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .build()
    }

    val apiService: ApiServices by lazy{
        retrofit.create(ApiServices::class.java)
    }
}

interface ApiServices {
    @POST("/restapi/login/")
    fun pushPostLogin(
        @Body post: UserModel
    ): Call<JwtModel>

    @POST("/restapi/upload/")
    fun pushPostMaterial(
        @Body post: MaterialUpModel,
        @Header("Authorization") Bearer: String,
    ): Call<MaterialTakeModel>

    @PUT
    fun postImage(
        @Url url: String?,
        @Body body: RequestBody,
        @Header("Authorization") Bearer: String,
    ): Call<ResponseBody?>?

    @GET("/restapi/subjects/")
    fun getSubjects(): Call<MutableList<SubjectModel>>
}

