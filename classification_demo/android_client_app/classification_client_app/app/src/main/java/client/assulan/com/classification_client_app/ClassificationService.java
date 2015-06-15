package client.assulan.com.classification_client_app;

import android.graphics.Bitmap;

import retrofit.Callback;
import retrofit.http.Field;
import retrofit.http.FormUrlEncoded;
import retrofit.http.Multipart;
import retrofit.http.POST;
import retrofit.http.Part;
import retrofit.mime.TypedFile;


public interface ClassificationService {
    @Multipart
    @POST("/")
    public void postImage(@Part("img") TypedFile img, Callback<Response> callback);


}


