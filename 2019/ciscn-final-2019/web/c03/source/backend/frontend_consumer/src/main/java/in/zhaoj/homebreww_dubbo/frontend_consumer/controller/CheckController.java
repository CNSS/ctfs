package in.zhaoj.homebreww_dubbo.frontend_consumer.controller;

import in.zhaoj.homebreww_dubbo.frontend_consumer.pojo.ResponseData;
import in.zhaoj.homebreww_dubbo.frontend_consumer.util.DubboCallUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author: ciscn
 * @date:2019-04-29
 * @description:
 */
@RestController
@RequestMapping("/api/check")
public class CheckController {

    @Autowired
    private DubboCallUtil dubboCallUtil;

    @GetMapping(value = "")
    public ResponseData show() throws IllegalStateException {
        return new ResponseData(ResponseData.CODE_SUCCESS, dubboCallUtil.getAllNodes());
    }
}
