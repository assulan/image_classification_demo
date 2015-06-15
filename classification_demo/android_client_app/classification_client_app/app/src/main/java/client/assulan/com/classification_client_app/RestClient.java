package client.assulan.com.classification_client_app;

import com.squareup.okhttp.OkHttpClient;

import java.util.concurrent.TimeUnit;

import retrofit.RestAdapter;
import retrofit.client.OkClient;


public class RestClient
{
//    private static final String BASE_URL = "http://10.0.2.2:8000";
//    private static final String BASE_URL = "http://192.168.43.10:8000/classify";
    private static final String BASE_URL = "http://192.168.0.104:8000/classify";

    private ClassificationService apiService;


    public RestClient()
    {
        OkHttpClient myClient = new OkHttpClient();
        myClient.setWriteTimeout(30, TimeUnit.SECONDS);
        RestAdapter restAdapter = new RestAdapter.Builder().setClient(new OkClient(myClient))
                .setEndpoint(BASE_URL)
                .build();

        apiService = restAdapter.create(ClassificationService.class);
    }

    public ClassificationService getApiService()
    {
        return apiService;
    }
}

