"""Authentication doctor checks for the control plane."""

from .collector import collect_doctor_checks

__all__ = ["collect_doctor_checks"]
