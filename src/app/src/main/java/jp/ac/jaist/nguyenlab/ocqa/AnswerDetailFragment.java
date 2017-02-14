package jp.ac.jaist.nguyenlab.ocqa;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.widget.NestedScrollView;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.RatingBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.PolylineOptions;

import java.lang.reflect.Field;
import java.util.List;

import jp.ac.jaist.nguyenlab.ocqa.data.Answer;
import jp.ac.jaist.nguyenlab.ocqa.data.CustomerReview;
import jp.ac.jaist.nguyenlab.ocqa.util.ScrollableSupportMapFragment;

//import com.google.android.gms.maps.GoogleMap;
//import com.google.android.gms.maps.SupportMapFragment;

/**
 * A fragment representing a single Answer detail screen.
 * This fragment is either contained in a {@link AnswerListActivity}
 * in two-pane mode (on tablets) or a {@link AnswerDetailActivity}
 * on handsets.
 */
public class AnswerDetailFragment extends Fragment implements GMapV2Direction.DirecitonReceivedListener {
    /**
     * The fragment argument representing the item ID that this fragment
     * represents.
     */
    public static final String ARG_ANSWER_URI = "answer_uri";
    public static final String ARG_ANSWER_IMAGE = "answer_image";

    /**
     * The dummy content this fragment is presenting.
     */
    private Answer answer;
    GoogleMap googleMap;
    FragmentManager myFragmentManager;
    ScrollableSupportMapFragment mySupportMapFragment;
    boolean isShowmap, isShowratingStar;
    float zoom = 15;
    /**
     * Mandatory empty constructor for the fragment manager to instantiate the
     * fragment (e.g. upon screen orientation changes).
     */
    public AnswerDetailFragment() {
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (getArguments().containsKey(ARG_ANSWER_URI)) {
            // Load the dummy content specified by the fragment
            // arguments. In a real-world scenario, use a Loader
            // to load content from a content provider.
            answer = QueryServiceClientAdapter.answerMap.get(getArguments().getString(ARG_ANSWER_URI));

            //Activity activity = this.getActivity();
            //CollapsingToolbarLayout appBarLayout = (CollapsingToolbarLayout) activity.findViewById(R.id.toolbar_layout);
            // if (appBarLayout != null) {
            //     appBarLayout.setTitle(answer.getName());
            // }
        }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.answer_detail, container, false);
        //
//        NONE,
//        PERSON,
//        PLACE,
//        ORGANIZATION,
//        ORGANIZATIONPLACE,
//         VALUE
        // Show the dummy content as text in a TextView.
        if (answer != null) {
            // show information
            //((TextView) rootView.findViewById(R.id.name)).setText("Name: " + answer.getName());
            //((TextView) rootView.findViewById(R.id.type)).setText("Type: " + answer.getEntType().toString());
            ((TextView) rootView.findViewById(R.id.name)).setText(answer.getName());
            ((TextView) rootView.findViewById(R.id.address)).setText("Address: " + answer.getAddress());
            ((TextView) rootView.findViewById(R.id.phone_number)).setText("Phone number: " + answer.getTelephoneNumber());
            ((TextView) rootView.findViewById(R.id.summary)).setText("Summary: " + answer.getSummary());
            ((TextView) rootView.findViewById(R.id.uri)).setText("Link: " + answer.getUri());
            // show image
            String picURL = answer.getPictureURL();

            new ImageLoadTask(picURL, (ImageView) rootView.findViewById(R.id.image)).execute();
//            if (getArguments().containsKey(ARG_ANSWER_IMAGE))
//            {
//                Bitmap b = BitmapFactory.decodeByteArray(
//                        getArguments().getByteArray(ARG_ANSWER_IMAGE),0, getArguments().getByteArray(ARG_ANSWER_IMAGE).length);
//                ((ImageView) rootView.findViewById(R.id.image)).setImageBitmap(b);
//            }
                // show customers' comments

            final ListView listView = (ListView) rootView.findViewById(R.id.customer_review_list);

            boolean isPlaceOrOrganization = answer.getEntType() == Answer.EntType.ORGANIZATIONPLACE || answer.getEntType() == Answer.EntType.ORGANIZATION || answer.getEntType() == Answer.EntType.PLACE;
            isShowratingStar = isPlaceOrOrganization;
            isShowmap = isPlaceOrOrganization;

            isShowmap = isShowmap && (answer.getGpsPosition().first !=0 || answer.getGpsPosition().second !=0);
            isShowratingStar &= answer.getNoOfReviews() > 0;
            if (isShowratingStar) {
                ((RatingBar) rootView.findViewById(R.id.avg_ratingBar)).setRating(answer.AvgScore());
                ((TextView) rootView.findViewById(R.id.numofcomments)).setText(answer.getNoOfReviews() + " Reviews");

                List<CustomerReview> reviews = answer.getCustomerReviews();
                if (reviews != null) {
                    CustomerReviewListAdapter adapter = new CustomerReviewListAdapter(getContext(), R.layout.customer_review_listitem, reviews);
                    listView.setAdapter(adapter);
                    adapter.notifyDataSetChanged();

                    // Setting the list height.
                    int totalItemsHeight = 0;
                    for (int itemPos = 0; itemPos < reviews.size(); itemPos++) {
                        View item = adapter.getView(itemPos, null, listView);
                        item.measure(0, 0);
                        totalItemsHeight += item.getMeasuredHeight();
                    }

                    int totalDividersHeight = listView.getDividerHeight() * (reviews.size() - 1);

                    ViewGroup.LayoutParams params = listView.getLayoutParams();
                    params.height = totalItemsHeight + totalDividersHeight;
                    listView.setLayoutParams(params);
                    listView.requestLayout();
                }
            } else {
                ((RatingBar) rootView.findViewById(R.id.avg_ratingBar)).setVisibility(View.GONE);
                ((TextView) rootView.findViewById(R.id.numofcomments)).setVisibility(View.GONE);
                listView.setVisibility(View.GONE);
            }

            final NestedScrollView scrollView = (NestedScrollView)container;

            if (scrollView != null) {
                scrollView.post(new Runnable() {
                    public void run() {
                        scrollView.scrollTo(0, 0);
                    }
                });
            }
        }
        // show google map
        initializeMap();
        if (isShowmap)
        {
            // Loading map
            //ShowCurrentLocation();
            ShowMap();
        }
        else
        {
            // remove the map
           ((ScrollableSupportMapFragment) getChildFragmentManager().findFragmentById(R.id.map)).getView().setVisibility(View.GONE);
        }

        return rootView;
    }

    private void ShowMap() {
        try {
            LatLng current_loc, dest_loc;
            // add marker
            dest_loc = new LatLng(answer.getGpsPosition().first, answer.getGpsPosition().second);
            googleMap.addMarker(new MarkerOptions()
                    .position(dest_loc)
                    .title(answer.getName()).icon((BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)))).showInfoWindow();

            // add marker of the user's location (if any)
            if(answer.getSource() == Answer.Source.GOOGLE_MAP) {
                current_loc = new LatLng(globalVar.currentLocation.getLatitude(), globalVar.currentLocation.getLongitude());
                googleMap.addMarker(new MarkerOptions()
                        .position(current_loc)
                        .title("Your location").icon((BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_GREEN))));

                boolean modeSelection = false;
                if (modeSelection) {
                    new GetRouteListTask(getContext(), current_loc,
                            dest_loc, GMapV2Direction.MODE_DRIVING, this)
                            .execute();
                } else {
                    new GetRouteListTask(getContext(), current_loc,
                            dest_loc, GMapV2Direction.MODE_WALKING, this)
                            .execute();
                }
            }

            googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(dest_loc, 15));


            if (ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
                // TODO: Consider calling
                //    ActivityCompat#requestPermissions
                // here to request the missing permissions, and then overriding
                //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
                //                                          int[] grantResults)
                // to handle the case where the user grants the permission. See the documentation
                // for ActivityCompat#requestPermissions for more details.
                //return rootView;
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void initializeMap() {
        try {
            if (googleMap == null) {
                myFragmentManager = getChildFragmentManager();//getActivity().getSupportFragmentManager();; // getFragmentManager();
                mySupportMapFragment = (ScrollableSupportMapFragment) myFragmentManager.findFragmentById(R.id.map);
                googleMap = mySupportMapFragment.getMap();

                googleMap.getUiSettings().setZoomControlsEnabled(true);
                googleMap.getUiSettings().setCompassEnabled(true);
                googleMap.getUiSettings().setMyLocationButtonEnabled(true);
                googleMap.getUiSettings().setMapToolbarEnabled(true);

                if (googleMap == null) {
                    Toast.makeText(getActivity().getApplicationContext(),
                            "Sorry! unable to create maps", Toast.LENGTH_SHORT)
                            .show();
                }

                final LinearLayout detailContainer = (LinearLayout) mySupportMapFragment.getView().getParent();
                mySupportMapFragment.setListener(new ScrollableSupportMapFragment.OnTouchListener() {
                    @Override
                    public void onTouch() {
                        detailContainer.requestDisallowInterceptTouchEvent(true);
                    }
                });
            }
        } catch (Exception e) {
            Toast.makeText(getActivity().getApplicationContext(), "" + e, Toast.LENGTH_LONG).show();
            // TODO: handle exception
        }
    }

    @Override
    public void onResume() {
        super.onResume();

        initializeMap();

    }

    @Override
    public void onDetach() {
        // TODO Auto-generated method stub
        super.onDetach();
        try {
            Field childFragmentManager = Fragment.class
                    .getDeclaredField("mChildFragmentManager");
            childFragmentManager.setAccessible(true);
            childFragmentManager.set(this, null);

        } catch (NoSuchFieldException e) {
            throw new RuntimeException(e);
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void OnDirectionListReceived(List<LatLng> mPointList) {
        if (mPointList != null) {
            PolylineOptions rectLine = new PolylineOptions().width(8).color(
                    Color.RED);
            for (int i = 0; i < mPointList.size(); i++) {
                rectLine.add(mPointList.get(i));
            }
            googleMap.addPolyline(rectLine);
        }
    }
}
