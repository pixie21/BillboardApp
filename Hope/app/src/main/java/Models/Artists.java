package Models;

public class Artists {
    public String name;
    public String artisturl;
    public int lastweek;
    public int peakpostion;
    public int weeksonchart;
    public boolean isNew;
    public int rank;

    public Artists() {

    }



    public Artists(String name, int lastweek, int peakpostion, int weeksonchart, boolean isNew, int rank, String artisturl) {
        this.name = name;
        this.lastweek = lastweek;
        this.peakpostion = peakpostion;
        this.weeksonchart = weeksonchart;
        this.isNew = isNew;
        this.rank = rank;
        this.artisturl = artisturl;

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getLastWeek() {
        return lastweek;
    }

    public void setLastweek(int lastweek) {
        this.lastweek = lastweek;
    }

    public int getPeakpostion() {
        return peakpostion; }

    public void setPeakpostion(int peakpostion) {
        this.peakpostion = peakpostion;
    }

    public int getWeeksonchart() {
        return weeksonchart;
    }

    public void setWeeksonchart(int weeksonchart) {
        this.weeksonchart = weeksonchart;
    }
    public boolean isNew() {
        return isNew;
    }

    public void setNew(boolean aNew) {
        isNew = aNew;
    }

    public int getRank() {
        return rank;
    }

    public void setRank(int rank) {
        this.rank = rank;
    }

    public String getArtisturl() {
        return artisturl;
    }

    public void setArtisturl(String artisturl) {
        this.artisturl = artisturl;
    }
}


