package com.iadh.iadh.service.impl;



import com.iadh.iadh.dto.request.UsersDTO;
import com.iadh.iadh.entity.Users;
import com.iadh.iadh.mapper.UsersMapper;
import com.iadh.iadh.repo.UsersRepository;
import com.iadh.iadh.service.UsersService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class UsersServiceImpl implements UsersService {

    @Autowired
    private UsersRepository userRepository;

    @Autowired
    private UsersMapper userMapper;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Override
    public String register(UsersDTO userDTO) throws IllegalArgumentException {
        if (userDTO == null || userDTO.getUsername() == null || userDTO.getPassword() == null) {
            throw new IllegalArgumentException("Username and password are required");
        }

        if (userRepository.findByUsername(userDTO.getUsername()) != null) {
            throw new IllegalArgumentException("Username already exists");
        }

        Users user = userMapper.toEntity(userDTO); // Hashes password and sets user_id
        userRepository.save(user);
        return user.getUserId();
    }

    @Override
    public String login(UsersDTO userDTO) throws IllegalArgumentException {
        if (userDTO == null || userDTO.getUsername() == null || userDTO.getPassword() == null) {
            throw new IllegalArgumentException("Username and password are required");
        }

        Users user = userRepository.findByUsername(userDTO.getUsername());
        if (user == null || !passwordEncoder.matches(userDTO.getPassword(), user.getPassword())) {
            throw new IllegalArgumentException("Invalid username or password");
        }

        return user.getUserId();
    }
}
