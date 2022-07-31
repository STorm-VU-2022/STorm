package storm.android.network

data class MaterialTakeModel (
    var id : Int,
    var title: String,
    var language: String = "English",
    var student_year: Int,
    var is_public: Boolean = true,
    var short_description: String,
    var description: String = short_description,
    var subject: Int,
    var media: String? = null,
)