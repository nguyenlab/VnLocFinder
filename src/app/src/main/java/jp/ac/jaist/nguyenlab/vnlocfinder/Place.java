package jp.ac.jaist.nguyenlab.vnlocfinder;

import android.location.Location;
import android.os.Parcel;
import android.os.Parcelable;
import android.util.Pair;

import jp.ac.jaist.nguyenlab.vnlocfinder.data.Answer;

public class Place implements Parcelable{
    // Latitude of the place
    public String mLat="";

    // Longitude of the place
    public String mLng="";

    // Place Name
    public String mPlaceName="";

    // Vicinity of the place
    public String mVicinity="";

    // Photos of the place
    // Photo is a Parcelable class
    public Photo[] mPhotos={};
    public  String mIcon="";

    @Override
    public int describeContents() {
        // TODO Auto-generated method stub
        return 0;
    }

    /** Writing Place object data to Parcel */
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(mLat);
        dest.writeString(mLng);
        dest.writeString(mPlaceName);
        dest.writeString(mVicinity);
        dest.writeString(mIcon);
        dest.writeParcelableArray(mPhotos, 0);
    }

    public Place(){
    }
    public Answer getAnswer()
    {
        Answer answer = new Answer();
        answer.setSource(Answer.Source.GOOGLE_MAP);
        answer.setEntType(Answer.EntType.PLACE);
        answer.setName(mPlaceName);
        if(mPhotos.length>0)
            answer.setPictureURL(mPhotos[0].getUrl());
        else
            answer.setPictureURL(mIcon);
        float vlat = Float.parseFloat(mLat);
        float vlong = Float.parseFloat(mLng);
        answer.setGpsPosition(new Pair<Float, Float>(vlat,vlong));
        answer.setAddress(mVicinity);
        // compute the distance from the user's location to the destination
        Location destloc = new Location("");
        destloc.setLatitude(vlat);
        destloc.setLongitude(vlong);
        float dis = destloc.distanceTo(globalVar.currentLocation);
        answer.setDistance(dis);
        answer.setSummary(String.format("Distance: %.1f km", dis/1000));
        answer.setUri(mPlaceName);

        return  answer;
    }
    /** Initializing Place object from Parcel object */
    private Place(Parcel in){
        this.mLat = in.readString();
        this.mLng = in.readString();
        this.mPlaceName = in.readString();
        this.mVicinity = in.readString();
        this.mIcon = in.readString();
        this.mPhotos = (Photo[])in.readParcelableArray(Photo.class.getClassLoader());
    }

    public static String getType(String info)
    {
        info = info.toLowerCase();
        if(info.contains("restaurant"))
            return  "restaurant";
        if(info.contains("hotel"))
            return  "hotel";
        if(info.contains("hospital"))
            return  "hospital";
        if(info.contains("airport"))
            return  "airport";
        return "";
    }
    /** Generates an instance of Place class from Parcel */
    public static final Parcelable.Creator<Place> CREATOR = new Parcelable.Creator<Place>(){
        @Override
        public Place createFromParcel(Parcel source) {
            return new Place(source);
        }

        @Override
        public Place[] newArray(int size) {
            // TODO Auto-generated method stub
            return null;
        }
    };
}