package in.zhaoj.homebreww_dubbo.frontend_consumer.pojo;

import com.fasterxml.jackson.annotation.JsonInclude;

/**
 * @author: ciscn
 * @date:2018/8/14
 * @description:回应数据
 */
@JsonInclude(JsonInclude.Include.NON_DEFAULT)
public class ResponseData {
    public static final int CODE_SUCCESS = 100;
    public static final int CODE_OPT_FAILED = 101;

    public static final int CODE_API_AUTH_REQUEST_EXPIRED = 203;
    public static final int CODE_API_AUTH_REQUEST_SIGNEDKEY_MISMATCH = 204;

    public static final int CODE_USER_UNREG = 301;
    public static final int CODE_USER_REG = 302;

    private int code;

    private Object data;

    private int count;

    public ResponseData(int code) {
        this.code = code;
    }

    public ResponseData(int code, Object data) {
        this.code = code;
        this.data = data;
    }

    public ResponseData(int code, Object data, int count) {
        this.code = code;
        this.data = data;
        this.count = count;
    }

    public int getCode() {
        return code;
    }

    public void setCode(int code) {
        this.code = code;
    }

    public Object getData() {
        return data;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public int getCount() {
        return count;
    }

    public void setCount(int count) {
        this.count = count;
    }
}
