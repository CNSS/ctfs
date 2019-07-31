package in.zhaoj.homebrew_dubbo.reg_center.pojo;

import java.util.Objects;

/**
 * @author: ciscn
 * @date:2019-07-02
 * @description:
 */
public class Node {
    private String ip;
    private int port;
    private boolean watchDog;

    public Node() {
        this.watchDog = true;
    }

    public Node(String ip, int port) {
        this.ip = ip;
        this.port = port;
        this.watchDog = true;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Node node = (Node) o;
        return port == node.port &&
                Objects.equals(ip, node.ip);
    }

    @Override
    public int hashCode() {
        return Objects.hash(ip, port);
    }

    public boolean isWatchDog() {
        return watchDog;
    }

    public void setWatchDog(boolean watchDog) {
        this.watchDog = watchDog;
    }
}
