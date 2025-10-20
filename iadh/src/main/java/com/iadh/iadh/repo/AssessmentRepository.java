package com.iadh.iadh.repo;



import com.iadh.iadh.entity.Assessment;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface AssessmentRepository extends JpaRepository<Assessment, Long> {
    List<Assessment> findByUserId(String userId);
}
