package jp.ac.jaist.nguyenlab.ocqa.ws;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.MySSLSocketFactory;
import com.loopj.android.http.RequestParams;

import java.util.HashMap;

//import cz.msebera.android.httpclient.conn.ssl.SSLSocketFactory;


public class WSClient {
    public enum BaseUrlKey {
        OCQA, MAPS;
    }
    private static final HashMap<BaseUrlKey, String> BASE_URL;

    static {
        BASE_URL = new HashMap<>();
        BASE_URL.put(BaseUrlKey.OCQA,"http://150.65.242.105:30000/qa_serv/"); // "http://150.65.242.90:34082/qa_serv/");
        BASE_URL.put(BaseUrlKey.MAPS, "https://maps.googleapis.com/maps/api/place/nearbysearch/json");
    }

    private static AsyncHttpClient client = new AsyncHttpClient();
    static
    {
        client.setSSLSocketFactory(MySSLSocketFactory.getFixedSocketFactory());
        /// initialize a default Keystore
        /*KeyStore trustStore = null;
        try {
            trustStore = KeyStore.getInstance(KeyStore.getDefaultType());

        // load the KeyStore
        trustStore.load(null, null);
        } catch (KeyStoreException e) {
            e.printStackTrace();
        } catch (CertificateException e) {
            e.printStackTrace();
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }*/
        //initialize a new SSLSocketFacrory
        /*MySSLSocketFactory socketFactory = null;
        try {
            socketFactory = new MySSLSocketFactory(MySSLSocketFactory.getKeystore());
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (KeyManagementException e) {
            e.printStackTrace();
        } catch (KeyStoreException e) {
            e.printStackTrace();
        } catch (UnrecoverableKeyException e) {
            e.printStackTrace();
        }
        //set that all host names are allowed in the socket factory
        socketFactory.setHostnameVerifier(MySSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);
        //initialize the Async Client
        if(client== null)
            client = new AsyncHttpClient();
        // We set the timeout to 10 seconds
        client.setTimeout(10*1000);
        // We set the SSL Factory
        client.setSSLSocketFactory(socketFactory);*/
    }
    public static void get(String url, BaseUrlKey key, RequestParams params, AsyncHttpResponseHandler responseHandler) {
       client.get(getAbsoluteUrl(url, key), params, responseHandler);
    }

    public static void post(String url, BaseUrlKey key, RequestParams params, AsyncHttpResponseHandler responseHandler) {
        client.post(getAbsoluteUrl(url, key), params, responseHandler);
    }

    private static String getAbsoluteUrl(String relativeUrl, BaseUrlKey key)
    {
        //return "http://150.65.242.59:34082/qa_serv/query?query=What%20is%20the%20closest%20indian%20restaurant%20to%20JAIST";
        //return "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=35.686817,139.772491&radius=5000&types=restaurant&sensor=true&key=AIzaSyC8L066x0qG8PMTELuxQRwLctC0wYhRXz0";
        return BASE_URL.get(key) + relativeUrl;
    }
}
/*class MySSLSocketFactory extends SSLSocketFactory {
    SSLContext sslContext = SSLContext.getInstance("TLS");

    public MySSLSocketFactory(KeyStore truststore) throws NoSuchAlgorithmException, KeyManagementException, KeyStoreException, UnrecoverableKeyException {
        super(truststore);

        TrustManager tm = new X509TrustManager() {
            public void checkClientTrusted(X509Certificate[] chain, String authType) throws CertificateException {
            }

            public void checkServerTrusted(X509Certificate[] chain, String authType) throws CertificateException {
            }

            public X509Certificate[] getAcceptedIssuers() {
                return null;
            }
        };

        sslContext.init(null, new TrustManager[] { tm }, null);
    }

    @Override
    public Socket createSocket(Socket socket, String host, int port, boolean autoClose) throws IOException, UnknownHostException {
        return sslContext.getSocketFactory().createSocket(socket, host, port, autoClose);
    }

    @Override
    public Socket createSocket() throws IOException {
        return sslContext.getSocketFactory().createSocket();
    }
}*/
