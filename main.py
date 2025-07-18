from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import phonenumbers
from phonenumbers.phonenumberutil import number_type, region_code_for_number
from phonenumbers import geocoder, timezone
from email_validator import validate_email as validate_email_lib, EmailNotValidError
import dns.resolver

app = FastAPI()

class PhoneRequest(BaseModel):
    phone_number: str

class EmailRequest(BaseModel):
    email: str

@app.post("/validate-phone")
def validate_phone(request: PhoneRequest):
    try:
        parsed = phonenumbers.parse(request.phone_number, None)
        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        is_formatted_properly = phonenumbers.is_possible_number_string(request.phone_number, None)
        country_code = parsed.country_code
        region_code = region_code_for_number(parsed)
        country = geocoder.country_name_for_number(parsed, "en")
        location = geocoder.description_for_number(parsed, "en")
        time_zones = timezone.time_zones_for_number(parsed)
        format_national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        format_international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        format_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        metadata = {
            "is_valid": is_valid,
            "is_formatted_properly": is_formatted_properly,
            "country": country,
            "location": location,
            "timezones": list(time_zones),
            "format_national": format_national,
            "format_international": format_international,
            "format_e164": format_e164,
            "country_code": country_code,
            "region_code": region_code,
            "type": number_type(parsed),
            "possible": is_possible,
            "national_number": parsed.national_number,
        }
        return metadata
    except phonenumbers.NumberParseException as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/validate-email")
def validate_email(request: EmailRequest):
    try:
        v = validate_email_lib(request.email, check_deliverability=True)
        # Check MX records
        mx_records = False
        try:
            answers = dns.resolver.resolve(v.domain, 'MX')
            mx_records = len(answers) > 0
        except Exception:
            mx_records = False
        metadata = {
            "local_part": v.local_part,
            "domain": v.domain,
            "ascii_email": v.ascii_email,
            "smtputf8": getattr(v, "smtputf8", None),
            "mx": getattr(v, "mx", None),
            "mx_records": mx_records,
        }
        # Only add these fields if not None
        display_name = getattr(v, "display_name", None)
        if display_name is not None:
            metadata["display_name"] = display_name
        mx_fallback_type = getattr(v, "mx_fallback_type", None)
        if mx_fallback_type is not None:
            metadata["mx_fallback_type"] = mx_fallback_type
        spf = getattr(v, "spf", None)
        if spf is not None:
            metadata["spf"] = spf
        return {"valid": True, "metadata": metadata}
    except EmailNotValidError as e:
        return {"valid": False, "metadata": {"error": str(e)}} 