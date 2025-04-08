from django.db import models
from django.contrib.auth.models import User
import uuid

class Code(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    code = models.TextField(
        help_text="Code content"
    )
    language = models.CharField(
        max_length=20,
        blank=True,
        help_text="The language in which the code is written. (C/C++)"
    )
    submittedBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Foreign Key of the User"
    )
    generatedReport = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Foreign Key of the Report"
    )

    def __str__(self):
        return f"Code by {self.submittedBy.username} - {self.language or 'Unknown Language'}"


class Vulnerability(models.Model):
    SEVERITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    cweId = models.CharField(
        max_length=50,
        help_text="CWE (Common Weakness Enumeration) identifier associated with this vulnerability"
    )
    cvssScore = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        help_text="CVSS (Common Vulnerability Scoring System) score, ranging from 0.0 to 10.0"
    )
    severity = models.CharField(
        max_length=6,
        choices=SEVERITY_CHOICES,
        help_text="Severity classification of the vulnerability"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the vulnerability"
    )
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
        help_text="Foreign Key of Code"
    )

    def __str__(self):
        return f"{self.cweId} - {self.severity} (Score: {self.cvssScore if self.cvssScore is not None else 'N/A'})"


class Exploit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the exploit and its intended behavior"
    )
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        related_name="exploits",
        help_text="Foreign Key of Code"
    )

    def __str__(self):
        return f"Exploit for Code ID: {self.code.id}"


class Patch(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    patchedCode = models.TextField(
        help_text="The secure version of the code after applying the patch"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed explanation of the patch and how it mitigates the vulnerability"
    )
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        related_name="patches",
        help_text="Foreign Key of Code"
    )

    def __str__(self):
        return f"Patch for Code ID: {self.code.id}"


class Report(models.Model):
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('HTML', 'HTML'),
        ('Markdown', 'Markdown'),
        ('Text', 'Text')
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    content = models.TextField(
        help_text="The content of the report"
    )
    format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        help_text="The format in which the report is generated (e.g., PDF, HTML, Markdown, Text)"
    )
    code = models.ForeignKey(
        Code,
        on_delete=models.CASCADE,
        related_name="reports",
        help_text="Foreign Key of Code"
    )

    def __str__(self):
        return f"Report for Code ID: {self.code.id} - Format: {self.format}"

