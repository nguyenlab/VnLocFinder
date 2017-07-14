package jp.ac.jaist.nguyenlab.vnlocfinder.data;

/**
 * Created by danilo on 2/23/16.
 */
public class CustomerReview {
    private float score;
    private String comments;
    public CustomerReview()
    {

    }
    public CustomerReview(float score, String comments)
    {
        this.score = score;
        this.comments = comments;
    }
    public float getScore() {
        return score;
    }

    public void setScore(float score) {
        this.score = score;
    }

    public String getComments() {
        return comments;
    }

    public void setComments(String comments) {
        this.comments = comments;
    }
}
