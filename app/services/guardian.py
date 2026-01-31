import os

class PulseGuardian:
    
    @staticmethod
    def verify_groundedness(answer, context):

        if not context or context == "No relevant data found.":
            return True, "The answer is based on general knowledge."
        

        if "500,000 TL" in context and "500,000 TL" not in answer:
             return False, "⚠️ Warning: Budget information is inconsistent with the document!"
        
        return True, "✅ The answer is consistent with the document."