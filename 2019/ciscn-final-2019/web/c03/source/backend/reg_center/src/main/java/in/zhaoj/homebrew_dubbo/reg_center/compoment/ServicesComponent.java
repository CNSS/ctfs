package in.zhaoj.homebrew_dubbo.reg_center.compoment;

import in.zhaoj.homebrew_dubbo.reg_center.pojo.Node;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

/**
 * @author: ciscn
 * @date:2019-07-02
 * @description:
 */
@Component
public class ServicesComponent {
    private HashMap<String, ArrayList<Node>> stringArrayListHashMap = new HashMap<>();

    public void regServiceNode(String serviceName, String ip, int port) {
        ArrayList<Node> arrayList = stringArrayListHashMap.getOrDefault(serviceName, new ArrayList<>());

        if(arrayList.contains(new Node(ip, port))) {
            arrayList.set(arrayList.indexOf(new Node(ip, port)), new Node(ip, port));
        } else {
            arrayList.add(new Node(ip, port));
        }

        stringArrayListHashMap.put(serviceName, arrayList);
    }

    public ArrayList<Node> pullServiceNode(String serviceName) {
        ArrayList<Node> arrayList = stringArrayListHashMap.getOrDefault(serviceName, new ArrayList<>());
        return arrayList;
    }

    public HashMap<String, ArrayList<Node>> pullAllServiceNode() {
        return stringArrayListHashMap;
    }

    @Scheduled(fixedDelay = 10000L)
    public void cleanDead() {
        Set<String> keySet = stringArrayListHashMap.keySet();
        for (String serviceName : keySet) {
            ArrayList<Node> arrayList = stringArrayListHashMap.getOrDefault(serviceName, new ArrayList<>());

            for (Iterator<Node> it = arrayList.iterator(); it.hasNext();) {
                Node node = it.next();
                if (!node.isWatchDog()) {
                    it.remove();
                } else {
                    node.setWatchDog(false);
                }
            }

            stringArrayListHashMap.put(serviceName, arrayList);
        }
    }
}
