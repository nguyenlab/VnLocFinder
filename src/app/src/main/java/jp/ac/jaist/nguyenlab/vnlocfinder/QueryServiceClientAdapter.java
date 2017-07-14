package jp.ac.jaist.nguyenlab.vnlocfinder;

import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.support.v4.app.FragmentManager;
import android.support.v7.widget.RecyclerView;
import android.util.Pair;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.TextView;

import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import cz.msebera.android.httpclient.Header;
import jp.ac.jaist.nguyenlab.vnlocfinder.data.Answer;
import jp.ac.jaist.nguyenlab.vnlocfinder.data.CustomerReview;
import jp.ac.jaist.nguyenlab.vnlocfinder.ws.WSClient;


public class QueryServiceClientAdapter
        extends RecyclerView.Adapter<QueryServiceClientAdapter.ViewHolder> {

    public static HashMap<String, Answer> answerMap;
    private List<Answer> answers;
    private FragmentManager suppFragManager;
    private boolean mTwoPane;

    QueryServiceClientAdapter(FragmentManager suppFragManager, boolean twoPane, boolean restoreState) {
        if (!restoreState) {
            answerMap = new HashMap<>();
            ImageLoadTask.cache = null;
        }

        this.suppFragManager = suppFragManager;
        mTwoPane = twoPane;
        //
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.answer_list_content, parent, false);

        answers = new ArrayList<>(answerMap.values());
        Collections.sort(answers);

        return new ViewHolder(view);
    }

    @Override
    public void onBindViewHolder(final ViewHolder holder, int position) {
        // show information of each answers
        Answer currentAns = answers.get(position);
        holder.answer = currentAns;
        // show image
        String picURL = currentAns.getPictureURL();

        new ImageLoadTask(picURL, holder.picture).execute();

        holder.name.setText(currentAns.getName());
        holder.summary.setText(currentAns.getSummary());

        if((currentAns.getEntType() == Answer.EntType.PLACE ||
                currentAns.getEntType() == Answer.EntType.ORGANIZATIONPLACE ||
                currentAns.getEntType() == Answer.EntType.ORGANIZATION) &&
                currentAns.getNoOfReviews() > 0)
        {
            holder.ratingBar.setRating(currentAns.AvgScore());
            holder.no_reviews.setText(currentAns.getNoOfReviews() + " Reviews");
        }
        else
            holder.review_layout.setVisibility(View.GONE);

        holder.mView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (mTwoPane) {
                    Bundle arguments = new Bundle();
                    // get parameters
                    arguments.putString(AnswerDetailFragment.ARG_ANSWER_URI, holder.answer.getName());
                    Bitmap bitmap = ((BitmapDrawable) holder.picture.getDrawable()).getBitmap();
                    ByteArrayOutputStream bs = new ByteArrayOutputStream();
                    bitmap.compress(Bitmap.CompressFormat.PNG, 50, bs);
                    arguments.putByteArray(AnswerDetailFragment.ARG_ANSWER_IMAGE, bs.toByteArray());

                    AnswerDetailFragment fragment = new AnswerDetailFragment();
                    fragment.setArguments(arguments);
                    suppFragManager.beginTransaction()
                            .replace(R.id.answer_detail_container, fragment)
                            .commit();
                } else {
                    Context context = v.getContext();
                    Intent intent = new Intent(context, AnswerDetailActivity.class);
                    // pass parameters
                    intent.putExtra(AnswerDetailFragment.ARG_ANSWER_URI, holder.answer.getUri());
//                    Bitmap bitmap = ((BitmapDrawable)holder.picture.getDrawable()).getBitmap();
//                    ByteArrayOutputStream bs = new ByteArrayOutputStream();
//                    bitmap.compress(Bitmap.CompressFormat.PNG, 50, bs);
//                    intent.putExtra(AnswerDetailFragment.ARG_ANSWER_IMAGE,bs.toByteArray());

                    context.startActivity(intent);
                }
            }
        });
    }

    @Override
    public int getItemCount() {
        if (answerMap != null) {
            return answerMap.size();
        }
        else {
            return 0;
        }
    }

    public class ViewHolder extends RecyclerView.ViewHolder {
        public final View mView;
        public final ImageView picture;
        public final TextView name;
        public final TextView summary;
        public RatingBar ratingBar;
        public TextView no_reviews;
        public LinearLayout review_layout;
        public Answer answer;

        public ViewHolder(View view) {
            super(view);
            mView = view;
            picture = (ImageView) view.findViewById(R.id.picture);
            name = (TextView) view.findViewById(R.id.name);
            summary = (TextView) view.findViewById(R.id.summary);
            ratingBar = (RatingBar)view.findViewById(R.id.rating_bar);
            no_reviews = (TextView)view.findViewById(R.id.no_reviews);
            review_layout = (LinearLayout)view.findViewById(R.id.review_layout);
        }

        @Override
        public String toString() {
            return super.toString() + " '" + name.getText() + "'";
        }
    }
    RequestParams getSearchNearByParams(String content)
    {
        String locInfo ="35.686817,139.772491";
        if(globalVar.currentLocation!=null) {

            locInfo = String.format("%f,%f",globalVar.currentLocation.getLatitude(), globalVar.currentLocation.getLongitude());
        }

        RequestParams params = new RequestParams();
        params.add("location",locInfo);
        params.add("radius", String.valueOf(globalVar.mRadius));
        params.add("types",Place.getType(content));
        params.add("name",content);
        params.add("sensor","true");
        params.add("key",globalVar.googleAPI_Key);
        return  params;
    }
    public void sendQuery(String query) throws JSONException {

        RequestParams params = new RequestParams();
        params.add("query", query);

        WSClient.get("query",WSClient.BaseUrlKey.OCQA , params, new JsonHttpResponseHandler()
        {
            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject response) {

            }
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONArray jsonAnswers) {
                try {
                    String map_searching_key ="";
                    boolean is_searching_around= false;
                    for (int i = 0; i < jsonAnswers.length(); i++) {
                        JSONObject jsonAnswer = jsonAnswers.getJSONObject(i);
                        Answer answer = new Answer();

                        answer.setName(jsonAnswer.getString("name"));
                        answer.setUri(jsonAnswer.getString("uri"));
                        if(answer.getUri().startsWith("gps"))
                        {
                            is_searching_around = true;
                            map_searching_key = answer.getName();
                            break;
                        }

                        answer.setPictureURL(jsonAnswer.getString("pictureURL"));
                        answer.setEntType(Answer.entTypeMap.get(jsonAnswer.getInt("entType")));
                        answer.setSummary(jsonAnswer.getString("summary"));

                        if (jsonAnswer.has("address")) {
                            answer.setAddress(jsonAnswer.getString("address"));
                        }

                        if (jsonAnswer.has("telephoneNumber")) {
                            answer.setTelephoneNumber(jsonAnswer.getString("telephoneNumber"));
                        }

                        if (jsonAnswer.has("gpsPosition")) {
                            JSONArray jsonGpsPos = jsonAnswer.getJSONArray("gpsPosition");
                            float lat = (float) jsonGpsPos.getDouble(0);
                            float lon = (float) jsonGpsPos.getDouble(1);
                            Pair<Float, Float> gpsPos = new Pair<Float, Float>(lat, lon);
                            answer.setGpsPosition(gpsPos);
                        }

                        if (jsonAnswer.has("customerReviews")) {
                            JSONArray jsonReviews = jsonAnswer.getJSONArray("customerReviews");
                            ArrayList<CustomerReview> customerReviews = new ArrayList<CustomerReview>();

                            for (int j = 0; j < jsonReviews.length(); j++) {
                                float score = (float) jsonReviews.getJSONObject(j).getDouble("score");
                                String comments = jsonReviews.getJSONObject(j).getString("comments");
                                CustomerReview cr = new CustomerReview();
                                cr.setScore(score);
                                cr.setComments(comments);
                                customerReviews.add(cr);
                            }

                            answer.setCustomerReviews(customerReviews);
                        }

                        answerMap.put(answer.getUri(), answer);
                    }

                    if(is_searching_around)
                    {
                        sendGoogleMapQuery(map_searching_key);
                    }
                    else
                        //notifyDataSetChanged();
                        showResults();

                } catch (JSONException jsonEx) {
                    System.out.println("Something went wrong with JSON");
                }
            }
        });
    }
    public void sendGoogleMapQuery(String content) throws JSONException {

        RequestParams params = new RequestParams();
        params = getSearchNearByParams(content);

        WSClient.get("",WSClient.BaseUrlKey.MAPS , params, new JsonHttpResponseHandler()
        {
            @Override
            public void onSuccess(int statusCode, Header[] headers, JSONObject response) {
                // If the response is JSONObject instead of expected JSONArray

                PlaceJSONParser parser = new PlaceJSONParser();
                Place[] places = parser.parse(response);
                List<Answer> answers = Answer.getListFromPlaces(places);

                for(Answer answer: answers)
                    answerMap.put(answer.getUri(), answer);
                //notifyDataSetChanged();
                showResults();
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, Throwable e, JSONObject response) {

            }
        });
    }
    public void showResults()
    {
        if(answerMap.size()==0)
        {
            // if no results were found. Add the default message
            Answer answer = new Answer();
            answer.setName("Sorry, no results were found");
            answer.setUri("Sorry, no results were found");
            //
            answerMap.put(answer.getUri(), answer);
        }
        notifyDataSetChanged();
    }
}
