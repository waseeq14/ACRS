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

    # TODO: Fix this. Change this to be a foreign key of the model Report.
    generatedReport = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Foreign Key of the Report"
    )

    def __str__(self):
        return f"Code by {self.submittedBy.username} - {self.language or 'Unknown Language'}"


class Vulnerability(models.Model):
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
    analysis_type = models.CharField(
        max_length=20,
        help_text="The type of analysis run to get the vulnerability",
        default="Analysis"
    )

    def __str__(self):
        return f"{self.cweId} - {self.code.language})"


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

class PentestProject(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    host = models.CharField(
        max_length=20,
        help_text="Host IP of the target machine"
    )
    username = models.CharField(
        max_length=50,
        help_text="Username of the target machine"
    )
    password = models.CharField(
        max_length=100,
        help_text="Password of the target machine"
    )
    scan_type = models.CharField(
        max_length=100,
        help_text="The scan type performed by the user"
    )
    submittedBy = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Foreign Key of the User"
    )

    def __str__(self):
        return f"{self.host} ({self.username})"

class PentestVulnerability(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    name = models.CharField(
        max_length=150,
        help_text="Name of the vulnerability"
    )
    description = models.TextField(
        help_text="The description of the vulnerability"
    )
    location = models.CharField(
        max_length=250,
        help_text="Location where the vulnerability exists"
    )
    cve = models.CharField(
        max_length=20,
        help_text="CVE Number"
    )
    project = models.ForeignKey(
        PentestProject,
        on_delete=models.CASCADE,
        related_name="vulnerabilities",
        help_text="Foreign Key of the Project"
    )

    def __str__(self):
        return f"{self.name} - {self.cve}"

class PentestExploit(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    description = models.TextField(
        help_text="The description of the exploit"
    )
    vulnerability = models.ForeignKey(
        PentestVulnerability,
        on_delete=models.CASCADE,
        related_name="exploits",
        help_text="Foreign Key of the Vulnerability"
    )

    def __str__(self):
        return f"Exploit for {self.vulnerability.name}"

class PentestPatch(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Primary Key"
    )
    description = models.TextField(
        help_text="The description of the patch"
    )
    vulnerability = models.ForeignKey(
        PentestVulnerability,
        on_delete=models.CASCADE,
        related_name="patches",
        help_text="Foreign Key of the Vulnerability"
    )
    def __str__(self):
        return f"Patch for {self.vulnerability.name}"