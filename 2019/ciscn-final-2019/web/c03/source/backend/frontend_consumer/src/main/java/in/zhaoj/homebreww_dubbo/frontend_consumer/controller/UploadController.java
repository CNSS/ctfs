package in.zhaoj.homebreww_dubbo.frontend_consumer.controller;

import in.zhaoj.homebreww_dubbo.frontend_consumer.pojo.DownloadFile;
import in.zhaoj.homebreww_dubbo.frontend_consumer.pojo.ResponseData;
import in.zhaoj.homebreww_dubbo.frontend_consumer.util.DubboCallUtil;
import in.zhaoj.homebreww_dubbo.frontend_consumer.util.FileSignUtil;
import org.apache.tomcat.util.codec.binary.Base64;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;

/**
 * @author: ciscn
 * @date:2019-04-29
 * @description:
 */
@RestController
@RequestMapping("/api/upload")
public class UploadController {

    @Autowired
    private DubboCallUtil dubboCallUtil;

    @Autowired
    private FileSignUtil fileSignUtil;

    @PostMapping(value = "")
    public ResponseData upload(MultipartFile file) throws IllegalStateException, IOException {
        String[] fileNames = file.getOriginalFilename().split("\\.");
        String fileName =  UUID.randomUUID() + "." + fileNames[fileNames.length - 1];
        String content = Base64.encodeBase64String(file.getBytes());

        HashMap<String, Object> requestHashMap = new HashMap<>();
        requestHashMap.put("filename", fileName);
        requestHashMap.put("content", content);

        HashMap<String, Object> returnHashMap = this.dubboCallUtil.callWithRetry("in.zhaoj.homebrew_dubbo.storage_provider.service.StorageService", "putFile", requestHashMap);

        returnHashMap.put("token", fileSignUtil.getToken(((String) returnHashMap.get("id")).getBytes()));

        return new ResponseData(ResponseData.CODE_SUCCESS, returnHashMap);
    }

    @GetMapping(value = "")
    public ResponseEntity<Resource> download(@RequestParam String token) throws IllegalStateException {
        byte[] id = fileSignUtil.verifyToken(token);

        if(id == null) {
            return ResponseEntity.notFound().build();
        }

        HashMap<String, Object> requestHashMap = new HashMap<>();
        requestHashMap.put("id", new String(id));

        HashMap<String, Object> returnHashMap = this.dubboCallUtil.callWithRetry("in.zhaoj.homebrew_dubbo.storage_provider.service.StorageService", "readFile", requestHashMap);

        try {
            Resource resource = new UrlResource((String) returnHashMap.get("url"));

            requestHashMap = new HashMap<>();
            requestHashMap.put("dictname", returnHashMap.get("dictname"));
            ResponseEntity<Resource> returnBody = ResponseEntity.ok()
                    .contentLength(resource.contentLength())
                    .header("Content-Disposition", "attachment; filename=" + returnHashMap.get("filename"))
                    .contentType(MediaType.parseMediaType("application/octet-stream"))
                    .body(resource);
            // this.dubboCallUtil.callWithRetry("in.zhaoj.homebrew_dubbo.storage_provider.service.StorageService", "deleteFile", requestHashMap);
            return returnBody;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    @GetMapping(value = "list")
    public ResponseData list() throws IllegalStateException {
        HashMap<String, Object> requestHashMap = new HashMap<>();

        HashMap<String, Object> returnHashMap = this.dubboCallUtil.callWithRetry("in.zhaoj.homebrew_dubbo.storage_provider.service.StorageService", "getFileLists", requestHashMap);

        ArrayList<DownloadFile> downloadFileArrayList = new ArrayList<>();
        ArrayList<String> originList = (ArrayList<String>) returnHashMap.get("data");
        for(String file : originList) {
            file = file.split("\\.")[0];
            downloadFileArrayList.add(new DownloadFile(file, fileSignUtil.getToken(file.getBytes())));
        }

        return new ResponseData(ResponseData.CODE_SUCCESS, downloadFileArrayList);
    }
}
