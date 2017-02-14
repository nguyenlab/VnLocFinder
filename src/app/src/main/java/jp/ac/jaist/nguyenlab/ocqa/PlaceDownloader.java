package jp.ac.jaist.nguyenlab.ocqa;

/**
 * Created by anhpv on 5/6/2016.
 */

import android.os.AsyncTask;
import android.util.Log;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;

/** A class, to download Google Places */
 class PlacesTask extends AsyncTask<String, Integer, String> {

    String data = null;
    QueryServiceClientAdapter viewHolder;
    public  PlacesTask(QueryServiceClientAdapter adapter)
    {
        this.viewHolder = viewHolder;
    }
    // Invoked by execute() method of this object
    @Override
    protected String doInBackground(String... url) {
        try{
            Log.d("URL:",url[0]);
            data = downloadUrl(url[0]);
        }catch(Exception e){
            Log.d("Background Task",e.toString());
        }
        return data;
    }

    // Executed after the complete execution of doInBackground() method
    @Override
    protected void onPostExecute(String result){
        ParserTask parserTask = new ParserTask(viewHolder);

        // Start parsing the Google places in JSON format
        // Invokes the "doInBackground()" method of ParserTask
        parserTask.execute(result);
    }
    /** A method to download json data from argument url */
    private String downloadUrl(String strUrl) throws IOException {
        String data = "";
        InputStream iStream = null;
        HttpURLConnection urlConnection = null;
        try{
            URL url = new URL(strUrl);


            // Creating an http connection to communicate with url
            urlConnection = (HttpURLConnection) url.openConnection();

            // Connecting to url
            urlConnection.connect();

            // Reading data from url
            iStream = urlConnection.getInputStream();

            BufferedReader br = new BufferedReader(new InputStreamReader(iStream));

            StringBuffer sb  = new StringBuffer();

            String line = "";
            while( ( line = br.readLine())  != null){
                sb.append(line);
            }

            data = sb.toString();

            br.close();

        }catch(Exception e){
            Log.d("Exception while downloading url", e.toString());
        }finally{
            iStream.close();
            urlConnection.disconnect();
        }
        return data;
    }

}

/** A class to parse the Google Places in JSON format */
class ParserTask extends AsyncTask<String, Integer, Place[]>{

    JSONObject jObject;
    List<Place> places;
    QueryServiceClientAdapter viewHolder;
    public ParserTask(QueryServiceClientAdapter viewHolder)
    {
        this.places = places;
        this.viewHolder = viewHolder;
    }
    // Invoked by execute() method of this object
    @Override
    protected Place[] doInBackground(String... jsonData) {


        Place[] places = null;
        PlaceJSONParser placeJsonParser = new PlaceJSONParser();

        try{
            jObject = new JSONObject(jsonData[0]);
            /** Getting the parsed data as a List construct */
            places = placeJsonParser.parse(jObject);
            this.places.clear();
            for(Place p: places)
                this.places.add(p);

        }catch(Exception e){
            Log.d("Exception",e.toString());
        }
        return places;
    }

    // Executed after the complete execution of doInBackground() method
    @Override
    protected void onPostExecute(Place[] places){

        int i=0;
        int x=0;
        x = 10/x;
        for (Place p: places) {
            i++;
            QueryServiceClientAdapter.answerMap.put(String.valueOf(i), p.getAnswer());
        }
        viewHolder.notifyDataSetChanged();
    }

}