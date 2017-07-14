package jp.ac.jaist.nguyenlab.vnlocfinder;

        import android.os.Parcel;
import android.os.Parcelable;

public class Photo implements Parcelable{

    // Width of the Photo
    int mWidth=0;

    // Height of the Photo
    int mHeight=0;

    // Reference of the photo to be used in Google Web Services
    String mPhotoReference="";

    // Attributions of the photo
    // Attribution is a Parcelable class
    Attribution[] mAttributions={};

    @Override
    public int describeContents() {
        // TODO Auto-generated method stub
        return 0;
    }

    /** Writing Photo object data to Parcel */
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeInt(mWidth);
        dest.writeInt(mHeight);
        dest.writeString(mPhotoReference);
        dest.writeParcelableArray(mAttributions, 0);

    }

    public Photo(){
    }
    public String getUrl()
    {
        StringBuilder url = new StringBuilder();
        url.append("https://maps.googleapis.com/maps/api/place/photo?");
        url.append("&key="); url.append(globalVar.googleAPI_Key);
        url.append("&sensor=true");
        url.append("&maxwidth="); url.append(globalVar.mWidthPhoto);
        url.append("&maxheight=");url.append(globalVar.mHeightPhoto);
        url.append("&photoreference=");url.append(mPhotoReference);
        return  url.toString();
    }
    /**  Initializing Photo object from Parcel object */
    private Photo(Parcel in){
        this.mWidth = in.readInt();
        this.mHeight = in.readInt();
        this.mPhotoReference = in.readString();
        this.mAttributions = (Attribution[])in.readParcelableArray(Attribution.class.getClassLoader());
    }

    /** Generates an instance of Place class from Parcel */
    public static final Parcelable.Creator<Photo> CREATOR = new Parcelable.Creator<Photo>() {
        @Override
        public Photo createFromParcel(Parcel source) {
            return new Photo(source);
        }

        @Override
        public Photo[] newArray(int size) {
            // TODO Auto-generated method stub
            return null;
        }
    };

}