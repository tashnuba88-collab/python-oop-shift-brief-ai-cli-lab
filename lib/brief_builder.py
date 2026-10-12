class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        """Build a prompt for creating a new shift handoff brief."""
        if notes is None or not str(notes).strip():
            raise ValueError("Shift notes cannot be empty.")

        sections = "\n".join(self.REQUIRED_SECTIONS)
        return (
            "Create a shift handoff brief from the shift notes below.\n"
            "Include every one of these section labels:\n"
            f"{sections}\n"
            "Do not invent unsupported details.\n"
            'Use "Unknown" when details are not provided.\n\n'
            f"Shift notes:\n{str(notes).strip()}"
        )

    def build_revision_prompt(self, feedback):
        """Build a prompt for revising the previous handoff brief."""
        if feedback is None or not str(feedback).strip():
            raise ValueError("Revision feedback cannot be empty.")

        sections = "\n".join(self.REQUIRED_SECTIONS)
        return (
            "Revise the previous handoff brief from our earlier conversation.\n"
            "Keep every one of these section labels:\n"
            f"{sections}\n"
            "Do not invent unsupported details.\n\n"
            f"Manager feedback:\n{str(feedback).strip()}"
        )

    def is_usable_brief(self, response_text):
        """Check whether the AI response includes the required structure."""
        if not isinstance(response_text, str) or not response_text.strip():
            return False
        return all(
            section in response_text for section in self.REQUIRED_SECTIONS
        )

    def format_brief(self, response_text):
        """Format a created handoff brief for display."""
        return f"\nShift Handoff Brief\n\n{response_text}"

    def create_brief(self, ai_client, notes):
        """Create a new handoff brief."""
        prompt = self.build_brief_prompt(notes)
        response = ai_client.send(prompt)
        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections."
            )
        return self.format_brief(response)

    def revise_brief(self, ai_client, feedback):
        """Revise the previous handoff brief."""
        prompt = self.build_revision_prompt(feedback)
        response = ai_client.send(prompt)
        if not self.is_usable_brief(response):
            raise RuntimeError(
                "AI response did not include required sections."
            )
        return f"\nRevised Shift Handoff Brief\n\n{response}"
