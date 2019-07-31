package in.zhaoj.homebreww_dubbo.frontend_consumer.compoment;

import in.zhaoj.homebreww_dubbo.frontend_consumer.pojo.Node;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * @author: ciscn
 * @date:2019-07-03
 * @description:
 */
@Component
public class ServiceComponent {
    private HashMap<String, Object> nodesHashMap;

    public ServiceComponent() {
        nodesHashMap = new HashMap<>();
    }

    public Node getNodeForService(String serviceName) {
        if(!nodesHashMap.containsKey(serviceName)) {
            return null;
        }

        ArrayList<HashMap<String, Object>> arrayList = (ArrayList<HashMap<String, Object>>) nodesHashMap.get(serviceName);

        int index = (int) (Math.random() * arrayList.size());
        HashMap<String, Object> linkedHashMap = arrayList.get(index);

        Node node = new Node();
        node.setIp((String) linkedHashMap.get("ip"));
        node.setPort((Integer) linkedHashMap.get("port"));

        return node;
    }

    public HashMap<String, Object> getNodesHashMap() {
        return nodesHashMap;
    }

    public void setNodesHashMap(HashMap<String, Object> nodesHashMap) {
        this.nodesHashMap = nodesHashMap;
    }
}
