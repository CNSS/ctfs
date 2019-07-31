package in.zhaoj.homebreww_dubbo.frontend_consumer.pojo;

/**
 * @author: ciscn
 * @date:2019-07-04
 * @description:
 */
public class DownloadFile {
    private String id;

    private String token;

    public DownloadFile() {
    }

    public DownloadFile(String id, String token) {
        this.id = id;
        this.token = token;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getToken() {
        return token;
    }

    public void setToken(String token) {
        this.token = token;
    }
}
