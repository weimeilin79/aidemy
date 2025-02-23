import os
from google import genai
from typing import TypedDict
from onramp_workaround import get_next_region
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")

MODEL_ID = "gemini-1.5-flash" 

class State(TypedDict):
    teaching_plan: str
    model_one_assignment: str
    model_two_assignment: str
    final_assignment: str

def gen_assignment_gemini(state):
    region=get_next_region()
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=region)
    print(f"---------------gen_assignment_gemini")
    response = client.models.generate_content(
        model=MODEL_ID, contents=f"""
        You are an instructor 

        Develop engaging and practical assignments for each week, ensuring they align with the teaching plan's objectives and progressively build upon each other.  

        For each week, provide the following:

        * **Week [Number]:** A descriptive title for the assignment (e.g., "Data Exploration Project," "Model Building Exercise").
        * **Learning Objectives Assessed:** List the specific learning objectives from the teaching plan that this assignment assesses.
        * **Description:** A detailed description of the task, including any specific requirements or constraints.  Provide examples or scenarios if applicable.
        * **Deliverables:** Specify what students need to submit (e.g., code, report, presentation).
        * **Estimated Time Commitment:**  The approximate time students should dedicate to completing the assignment.
        * **Assessment Criteria:** Briefly outline how the assignment will be graded (e.g., correctness, completeness, clarity, creativity).

        The assignments should be a mix of individual and collaborative work where appropriate.  Consider different learning styles and provide opportunities for students to apply their knowledge creatively.

        Based on this teaching plan: {state["teaching_plan"]}
        """
    )

    print(f"---------------gen_assignment_gemini answer {response.text}")
    
    state["model_one_assignment"] = response.text
    
    return state

def combine_assignments(state):
    print(f"---------------combine_assignments ")
    region=get_next_region()
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=region)
    response = client.models.generate_content(
        model=MODEL_ID, contents=f"""
        Look at all the proposed assignment so far {state["model_one_assignment"]} and {state["model_two_assignment"]}, combine them and come up with a final assignment for student. 
        """
    )

    state["final_assignment"] = response.text
    
    return state

import unittest

class TestGenAssignmentGemini(unittest.TestCase):
    def test_gen_assignment_gemini(self):
        test_teaching_plan = "Week 1: 2D Shapes and Angles - Day 1: Review of basic 2D shapes (squares, rectangles, triangles, circles). Day 2: Exploring different types of triangles (equilateral, isosceles, scalene, right-angled). Day 3: Exploring quadrilaterals (square, rectangle, parallelogram, rhombus, trapezium). Day 4: Introduction to angles: right angles, acute angles, and obtuse angles. Day 5: Measuring angles using a protractor. Week 2: 3D Shapes and Symmetry - Day 6: Introduction to 3D shapes: cubes, cuboids, spheres, cylinders, cones, and pyramids. Day 7: Describing 3D shapes using faces, edges, and vertices. Day 8: Relating 2D shapes to 3D shapes. Day 9: Identifying lines of symmetry in 2D shapes. Day 10: Completing symmetrical figures. Week 3: Position, Direction, and Problem Solving - Day 11: Describing position using coordinates in the first quadrant. Day 12: Plotting coordinates to draw shapes. Day 13: Understanding translation (sliding a shape). Day 14: Understanding reflection (flipping a shape). Day 15: Problem-solving activities involving perimeter, area, and missing angles."
        
        initial_state = {"teaching_plan": test_teaching_plan, "model_one_assignment": "", "model_two_assigmodel_one_assignmentnment": "", "final_assignment": ""}

        updated_state = gen_assignment_gemini(initial_state)

        self.assertIn("model_one_assignment", updated_state)
        self.assertIsNotNone(updated_state["model_one_assignment"])
        self.assertIsInstance(updated_state["model_one_assignment"], str)
        self.assertGreater(len(updated_state["model_one_assignment"]), 0)
        print(updated_state["model_one_assignment"])


if __name__ == '__main__':
    unittest.main()
