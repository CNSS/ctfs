package in.zhaoj.homebrew_dubbo.storage_provider.service.Impl;

import in.zhaoj.homebrew_dubbo.storage_provider.service.StorageService;
import in.zhaoj.homebrew_dubbo.storage_provider.util.FileUtil;
import in.zhaoj.homebrew_dubbo.storage_provider.util.ShellUtil;
import org.apache.tomcat.util.codec.binary.Base64;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.UUID;

/**
 * @author: ciscn
 * @date:2019-07-03
 * @description:
 */
@Component
public class StorageServiceImpl implements StorageService {

    @Value("${file.staticAccessPath}")
    private String staticAccessPath;

    @Value("${hb_dubbo.bind-address}")
    private String host;

    @Value("${server.port}")
    private String port;

    @Value("${file.uploadFolder}")
    private String uploadFolder;

    @Value("${file.tmpPath}")
    private String tmpPath;

    @Autowired
    private ShellUtil shellUtil;

    @Autowired
    private FileUtil fileUtil;

    @Override
    public HashMap<String, Object> putFile(HashMap<String, Object> parameter) {
        HashMap<String, Object> returnHashMap = new HashMap<>();

        String[] fileNames = ((String)(parameter.get("filename"))).split("\\.");
        if(fileNames[fileNames.length - 1].length() > 4) {
            fileNames[fileNames.length - 1] = fileNames[fileNames.length - 1].substring(0, 4);
        }
        String fileName =  UUID.randomUUID() + "." + fileNames[fileNames.length - 1];
        byte[] data = Base64.decodeBase64(((String)(parameter.get("content"))));
        try {
            try (OutputStream stream = new FileOutputStream(uploadFolder + '/' + fileName)) {
                stream.write(data);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        String zipFileName = String.valueOf(UUID.randomUUID());

        shellUtil.exec("cd " + uploadFolder + " && zip " + zipFileName + ".zip " + fileName + " && rm -f " + uploadFolder + '/' + fileName);

        returnHashMap.put("id", zipFileName);

        return returnHashMap;
    }

    @Override
    public HashMap<String, Object> getFileLists(HashMap<String, Object> parameter) {
        HashMap<String, Object> returnHashMap = new HashMap<>();

        List<String> result = new ArrayList<>();
        fileUtil.list(new File(uploadFolder  + "/"), result);
        returnHashMap.put("data", result);

        return returnHashMap;
    }

    @Override
    public HashMap<String, Object> deleteFile(HashMap<String, Object> parameter) {
        HashMap<String, Object> returnHashMap = new HashMap<>();

        String dictName = ((String)(parameter.get("dictname")));

        new Thread() {
            @Override
            public void run() {
                super.run();
                try {
                    sleep(60 * 1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                fileUtil.deleteDir(new File(tmpPath + "/" + dictName + "/"));
            }
        }.start();

        return returnHashMap;
    }

    @Override
    public HashMap<String, Object> readFile(HashMap<String, Object> parameter) {
        HashMap<String, Object> returnHashMap = new HashMap<>();

        String id = ((String)(parameter.get("id")));
        String dictName = String.valueOf(UUID.randomUUID());

        shellUtil.exec("cd " + uploadFolder + " && unzip " + id + ".zip -d " + tmpPath + "/" + dictName + "/");

        List<String> result = new ArrayList<>();
        fileUtil.list(new File(tmpPath + "/" + dictName + "/"), result);
        String[] fileNames = result.get(0).split("/");
        returnHashMap.put("filename", fileNames[fileNames.length - 1]);
        returnHashMap.put("dictname", dictName);
        returnHashMap.put("size", new File(tmpPath + "/" + dictName + "/" + fileNames[fileNames.length - 1]).length());
        returnHashMap.put("url", "http://" + host + ":" + port + "/" + staticAccessPath.replace("**", "") + "/" + dictName + "/" + fileNames[fileNames.length - 1]);

        shellUtil.exec( "rm -rf " + uploadFolder + "/" + dictName + "/");

        return returnHashMap;
    }
}
