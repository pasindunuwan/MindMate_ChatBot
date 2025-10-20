package com.iadh.iadh.service;



import com.iadh.iadh.dto.request.AssessmentDTO;

import java.util.List;

public interface AssessmentService {

    void saveAssessment(AssessmentDTO assessmentDTO) throws IllegalArgumentException;

    List<AssessmentDTO> getAssessmentsByUserId(String userId) throws IllegalArgumentException;
}