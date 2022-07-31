package storm.android.network

data class MaterialUpModel (
    var title: String,
    var language: String = "English",
    var student_year: Int,
    var is_public: String = "True",
    var short_description: String,
    var description: String = short_description,
    var subject: Int,
)