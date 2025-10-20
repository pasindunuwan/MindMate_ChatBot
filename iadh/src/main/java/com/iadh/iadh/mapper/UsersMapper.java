package com.iadh.iadh.mapper;



import com.iadh.iadh.dto.request.UsersDTO;
import com.iadh.iadh.entity.Users;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.stereotype.Component;

import java.util.UUID;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
@Component
public class UsersMapper {

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    // Map UserDTO to User (for registration)
    public Users toEntity(UsersDTO userDTO) {
        if (userDTO == null) {
            throw new IllegalArgumentException("UserDTO cannot be null");
        }
        Users user = new Users();
        user.setUserId(UUID.randomUUID().toString());
        user.setUsername(userDTO.getUsername());
        user.setPassword(passwordEncoder.encode(userDTO.getPassword()));
        return user;
    }

    // Map User to UserDTO (for response, excluding password)
    public UsersDTO toDto(Users user) {
        if (user == null) {
            throw new IllegalArgumentException("User cannot be null");
        }
        UsersDTO userDTO = new UsersDTO();
        userDTO.setUsername(user.getUsername());
        // Password is not included in the response for security
        return userDTO;
    }

    // Map UserDTO to User for login (no user_id generation, only for validation)
    public Users toEntityForLogin(UsersDTO userDTO) {
        if (userDTO == null) {
            throw new IllegalArgumentException("UserDTO cannot be null");
        }
        Users user = new Users();
        user.setUsername(userDTO.getUsername());
        user.setPassword(userDTO.getPassword()); // Plain-text password, to be verified
        return user;
    }
}