package com.iadh.iadh.service;

import com.iadh.iadh.dto.request.UsersDTO;

public interface UsersService {

    String register(UsersDTO userDTO) throws IllegalArgumentException;

    String login(UsersDTO userDTO) throws IllegalArgumentException;
}
