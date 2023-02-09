package com.famillink.controller;

import com.famillink.model.domain.user.Member;
import com.famillink.model.service.EmitterService;
import com.famillink.model.service.SseService;
import io.swagger.annotations.ApiOperation;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;


@RestController
@RequiredArgsConstructor
@RequestMapping("/sse")
public class SseController {

    private final SseService sseService;

    private final EmitterService emitterService;

    @ApiOperation(value = "알림 구독", notes = "알림을 구독한다.")
    @GetMapping(value = "/subscribe", produces = "text/event-stream")
    @ResponseStatus(HttpStatus.OK)
    public SseEmitter subscribe(@RequestHeader(value = "Last-Event-ID", required = false, defaultValue = "") String lastEventId){
        //Authentication authentication, @RequestHeader(value = "Last-Event-ID", required = false, defaultValue = "") String lastEventId

        //Member member = (Member) authentication.getPrincipal();

        return sseService.subscribe(1L, lastEventId);
    }

    @ApiOperation(value = "알림 구독 해제", notes = "알림을 구독을 해제한다.")
    @GetMapping(value = "/logout", produces = "text/event-stream")
    @ResponseStatus(HttpStatus.OK)
    public void logout(Long member_uid){

        emitterService.deleteAllEmitterStartWithMemberUid(member_uid);
        emitterService.deleteAllEventCacheStartWithId(member_uid);

    }

//    @ApiOperation(value = "알림 구독 해제", notes = "알림을 구독을 해제한다.")
//    @GetMapping(value = "/send", produces = "text/event-stream")
//    @ResponseStatus(HttpStatus.OK)
//    public void send(Long member_uid){
//
//        sseService.send(1L, "content", "localhost:9999");
//
//    }

}