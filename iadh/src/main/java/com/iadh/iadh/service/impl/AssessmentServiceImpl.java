package com.iadh.iadh.service.impl;




import com.iadh.iadh.dto.request.AssessmentDTO;
import com.iadh.iadh.entity.Assessment;
import com.iadh.iadh.mapper.AssessmentMapper;
import com.iadh.iadh.repo.AssessmentRepository;
import com.iadh.iadh.repo.UsersRepository;
import com.iadh.iadh.service.AssessmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class AssessmentServiceImpl implements AssessmentService {

    @Autowired
    private AssessmentRepository assessmentRepository;

    @Autowired
    private AssessmentMapper assessmentMapper;

    @Autowired
    private UsersRepository userRepository;

    @Override
    public void saveAssessment(AssessmentDTO assessmentDTO) throws IllegalArgumentException {
        if (assessmentDTO == null || assessmentDTO.getUserId() == null ||
                assessmentDTO.getScore() == null || assessmentDTO.getLevel() == null) {
            throw new IllegalArgumentException("Assessment fields cannot be null");
        }

        if (userRepository.findById(assessmentDTO.getUserId()).isEmpty()) {
            throw new IllegalArgumentException("User ID does not exist");
        }

        Assessment assessment = assessmentMapper.toEntity(assessmentDTO);
        assessmentRepository.save(assessment);
    }

    @Override
    public List<AssessmentDTO> getAssessmentsByUserId(String userId) throws IllegalArgumentException {
        if (userId == null) {
            throw new IllegalArgumentException("User ID cannot be null");
        }

        if (userRepository.findById(userId).isEmpty()) {
            throw new IllegalArgumentException("User ID does not exist");
        }

        List<Assessment> assessments = assessmentRepository.findByUserId(userId);
        return assessments.stream()
                .map(assessmentMapper::toDto)
                .collect(Collectors.toList());
    }
}