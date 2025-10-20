package com.iadh.iadh.controller;


import com.iadh.iadh.dto.request.UsersDTO;
import com.iadh.iadh.service.UsersService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;



@RestController
@RequestMapping("/api/auth")
public class UsersController {

    @Autowired
    private UsersService userService;

    @PostMapping("/register")
    public ResponseEntity<String> register(@Valid @RequestBody UsersDTO userDTO) {
        try {
            String userId = userService.register(userDTO);
            return ResponseEntity.ok("Registration successful! User ID: " + userId);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(400).body(e.getMessage());
        }
    }

    @PostMapping("/login")
    public ResponseEntity<String> login(@Valid @RequestBody UsersDTO userDTO) {
        try {
            String userId = userService.login(userDTO);
            return ResponseEntity.ok("Login successful! User ID: " + userId);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(401).body(e.getMessage());
        }
    }
}
