/**
 * Created by Danilo <danilo@jaist.ac.jp> on 1/23/16.
 */
package jp.ac.jaist.nguyenlab.vnlocfinder.data;

import android.util.Pair;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import jp.ac.jaist.nguyenlab.vnlocfinder.Place;
import jp.ac.jaist.nguyenlab.vnlocfinder.ws.WSClient;


public class Answer implements Comparable<Answer> {
    private Source source =Source.NGUYENLAB_SERVER;
    private String name;
    private EntType entType;
    private String pictureURL;
    private String uri;
    private String summary;
    private String address;
    private String telephoneNumber;
    private Pair<Float, Float> gpsPosition;
    private List<CustomerReview> customerReviews;
    private  CustomerReview overall = null;
    private float distance=0; // distance to current location (in meter)

    @Override
    public int compareTo(Answer another) {
        int sign = 0;
        if (distance>another.distance)
            sign = 1;
        if (distance<another.distance)
            sign =  -1;

        if (sign == 0 && overall != null && another.overall != null) {
            if (overall.getScore() < another.overall.getScore()) {
                sign = 1;
            }
            else if (overall.getScore() > another.overall.getScore()) {
                sign = -1;
            }
        }

        return sign;
    }

    public enum EntType {
        NONE,
        PERSON,
        PLACE,
        ORGANIZATION,
        ORGANIZATIONPLACE,
        VALUE
    }
    public enum Source
    {
        NGUYENLAB_SERVER,
        GOOGLE_MAP
    }
    public static  final List<Answer> getListFromPlaces(Place[] places)
    {
        List<Answer> answers = new ArrayList<>();
        for (Place p: places)
        {
            answers.add(answers.size(), p.getAnswer());
        }
        return  answers;
    }
    public static final  Map<Integer, EntType> entTypeMap;
    static {
        Map<Integer, EntType> initMap = new HashMap<>();
        initMap.put(0, EntType.NONE);
        initMap.put(1, EntType.PERSON);
        initMap.put(2, EntType.PLACE);
        initMap.put(4, EntType.ORGANIZATION);
        initMap.put(6, EntType.ORGANIZATIONPLACE);
        initMap.put(8, EntType.VALUE);

        entTypeMap = Collections.unmodifiableMap(initMap);
    }


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public EntType getEntType() {
        return entType;
    }

    public void setEntType(EntType entType) {
        this.entType = entType;
    }

    public String getPictureURL() {
        return WSClient.BASE_URL.get(WSClient.BaseUrlKey.IMG) + pictureURL;
    }

    public void setDistance(float distance) {
        this.distance = distance;
    }

    public float getDistance() {
        return distance;
    }

    public void setPictureURL(String pictureURL) {
        this.pictureURL = pictureURL;
    }
    public Source getSource(){return  source;}
    public void setSource(Source source){this.source = source;}
    public String getUri() {
        return uri;
    }

    public void setUri(String uri) {
        this.uri = uri;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getTelephoneNumber() {
        return telephoneNumber;
    }

    public void setTelephoneNumber(String telephoneNumber) {
        this.telephoneNumber = telephoneNumber;
    }

    public Pair<Float, Float> getGpsPosition() {
        return gpsPosition;
    }

    public void setGpsPosition(Pair<Float, Float> gpsPosition) {
        this.gpsPosition = gpsPosition;
    }

    public List<CustomerReview> getCustomerReviews()
    {
        return customerReviews;
    }

    public void setCustomerReviews(List<CustomerReview> customerReviews) {

        if(customerReviews != null && customerReviews.size()>0) {
            if (customerReviews.get(customerReviews.size() - 1).getComments().compareTo("OVERALL")==0)
                overall = customerReviews.get(customerReviews.size() - 1);
            customerReviews.remove(customerReviews.size() - 1);
        }
        this.customerReviews = customerReviews;
    }
    public int getNoOfReviews()
    {
        if(customerReviews==null) return 0;
        return customerReviews.size();
    }

    public float AvgScore()
    {
        if(overall!= null)
            return  overall.getScore();
        if(customerReviews==null) return 0f;

        float score = 0f;
        for(CustomerReview cm: customerReviews)
            score += cm.getScore();
        if(customerReviews.size()>0)
            score/= customerReviews.size();
        return score;
    }

}
