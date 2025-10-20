package com.iadh.iadh.mapper;



import com.iadh.iadh.dto.request.AssessmentDTO;
import com.iadh.iadh.entity.Assessment;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class AssessmentMapper {

    // Map AssessmentDTO to Assessment (for saving results)
    public Assessment toEntity(AssessmentDTO assessmentDTO) {
        if (assessmentDTO == null || assessmentDTO.getUserId() == null ||
                assessmentDTO.getScore() == null || assessmentDTO.getLevel() == null) {
            throw new IllegalArgumentException("AssessmentDTO fields cannot be null");
        }
        Assessment assessment = new Assessment();
        assessment.setUserId(assessmentDTO.getUserId());
        assessment.setScore(assessmentDTO.getScore());
        assessment.setLevel(assessmentDTO.getLevel());
        assessment.setTimestamp(LocalDateTime.now());
        return assessment;
    }

    // Map Assessment to AssessmentDTO (for response, e.g., charting)
    public AssessmentDTO toDto(Assessment assessment) {
        if (assessment == null) {
            throw new IllegalArgumentException("Assessment cannot be null");
        }
        AssessmentDTO assessmentDTO = new AssessmentDTO();
        assessmentDTO.setUserId(assessment.getUserId());
        assessmentDTO.setScore(assessment.getScore());
        assessmentDTO.setLevel(assessment.getLevel());
        assessmentDTO.setTimestamp(assessment.getTimestamp());
        return assessmentDTO;
    }
}
