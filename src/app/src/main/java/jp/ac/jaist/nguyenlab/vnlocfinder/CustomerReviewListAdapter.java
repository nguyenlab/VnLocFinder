package jp.ac.jaist.nguyenlab.vnlocfinder;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.TextView;

import java.util.List;

import jp.ac.jaist.nguyenlab.vnlocfinder.data.CustomerReview;

/**
 * Created by anhpv on 3/15/2016.
 */
public class CustomerReviewListAdapter extends ArrayAdapter<CustomerReview> {
    //private List<CustomerReview> listData;
    //private LayoutInflater layoutInflater;
    int resource;

//    public CustomerReviewListAdapter(LayoutInflater inflater, List<CustomerReview> listData) {
//        this.listData = listData;
//        layoutInflater = inflater;
//    }
    public CustomerReviewListAdapter(Context context, int resource, List<CustomerReview> listData) {
        super(context, resource, listData);
        //this.listData = listData;
        this.resource = resource;
    }
//    @Override
//    public int getCount() {
//        return listData.size();
//    }

    //@Override
//    public Object getItem(int position) {
//        return listData.get(position);
//    }

//    @Override
//    public long getItemId(int position) {
//        return position;
//    }
    @Override
    public View getView(int position, View convertView, ViewGroup parent)
    {
        LinearLayout alertView;
        //Get the current alert object
        CustomerReview review = getItem(position);

        //Inflate the view
        if(convertView==null)
        {
            alertView = new LinearLayout(getContext());
            String inflater = Context.LAYOUT_INFLATER_SERVICE;
            LayoutInflater vi;
            vi = (LayoutInflater)getContext().getSystemService(inflater);
            vi.inflate(resource, alertView, true);
        }
        else
        {
            alertView = (LinearLayout) convertView;
        }
        //Get the text boxes from the listitem.xml file
        RatingBar ratingBar =(RatingBar)alertView.findViewById(R.id.ratingBar);
        TextView comments =(TextView)alertView.findViewById(R.id.comments);

        //Assign the appropriate data from our alert object above
        ratingBar.setRating(review.getScore());
        comments.setText(review.getComments());

        return alertView;
    }
//    public View getView(int position, View convertView, ViewGroup parent) {
//        if (convertView == null) {
//            convertView = layoutInflater.inflate(R.layout.customer_review_listitem, null);
//            holder = new ViewHolder();
//            holder.ratingBar = (RatingBar) convertView.findViewById(R.id.ratingBar);
//            holder.comments = (TextView) convertView.findViewById(R.id.comments);
//
//            convertView.setTag(holder);
//
//        } else {
//            holder = (ViewHolder) convertView.getTag();
//        }
//
//        CustomerReview review = listData.get(position);
//        holder.ratingBar.setRating(review.getScore());
//        holder.comments.setText(review.getComments());
//
//        return convertView;
//    }
}
