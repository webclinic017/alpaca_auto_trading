from enum import Enum



class ExtendedEnum(Enum):

    @classmethod
    @property
    def choices(cls):
        return tuple(map(lambda c: (c.name,c.value), cls))
    
    
    @classmethod
    def to_dict(cls):
        data ={}
        for c in cls:
            data[c.name] = c.value
        return data
    


        
        
class AccountStatus(ExtendedEnum):
    SUBMITTED="Application has been submitted and in process of review"
    ACTION_REQUIRED="Application requires manual action"
    EDITED="Application was edited (e.g. to match info from uploaded docs). This is a transient status."
    APPROVAL_PENDING="Initial value. Application approval process is in process"
    APPROVED="Account application has been approved, waiting to be ACTIVE"
    REJECTED="Account application is rejected"
    ACTIVE="Account is fully active. Trading and funding can only be processed if an account is ACTIVE."
    DISABLED="Account is disabled, comes after ACTIVE"
    ACCOUNT_CLOSED="Account is closed"
    
class Agreement(ExtendedEnum):
    MA ="margin_agreement"
    AA ="account_agreement"
    CA ="customer_agreement"
    
class DocumentType(ExtendedEnum):
    identity_verification="Identity verification"
    address_verification="Address verification"
    date_of_birth_verification="Date of birth verification"
    tax_id_verification="Tax ID verification"
    account_approval_letter="407 approval letter"
    w8ben="W-8 BEN tax form"
    
    
    
class Employment(ExtendedEnum):
    unemployed="Unemployed"
    employed="Employed"
    student="Student"
    retired="Retired"
    
class FundingSource(ExtendedEnum):
    employment_income="Employment income"
    investments="Investments"
    inheritance="Inheritance"
    business_income="Business income"
    savings="Savings"
    family="Family"

class TaxIdType(ExtendedEnum):
    USA_SSN="USA Social Security Number"
    ARG_AR_CUIT="Argentina CUIT"
    AUS_TFN="Australian Tax File Number"
    AUS_ABN="Australian Business Number"
    BOL_NIT="Bolivia NIT"
    BRA_CPF="Brazil CPF"
    CHL_RUT="Chile RUT"
    COL_NIT="Colombia NIT"
    CRI_NITE="Costa Rica NITE"
    DEU_TAX_ID="Germany Tax ID (Identifikationsnummer)"
    DOM_RNC="Dominican Republic RNC"
    ECU_RUC="Ecuador RUC"
    FRA_SPI="France SPI (Reference Tax Number)"
    GBR_UTR="UK UTR (Unique Taxpayer Reference)"
    GBR_NINO="UK NINO (National Insurance Number)"
    GTM_NIT="Guatemala NIT"
    HND_RTN="Honduras RTN"
    HUN_TIN="Hungary TIN Number"
    IDN_KTP="Indonesia KTP"
    IND_PAN="India PAN Number"
    ISR_TAX_ID="Israel Tax ID (Teudat Zehut)"
    ITA_TAX_ID="Italy Tax ID (Codice Fiscale)"
    JPN_TAX_ID="Japan Tax ID (Koijin Bango)"
    MEX_RFC="Mexico RFC"
    NIC_RUC="Nicaragua RUC"
    NLD_TIN="Netherlands TIN Number"
    PAN_RUC="Panama RUC"
    PER_RUC="Peru RUC"
    PRY_RUC="Paraguay RUC"
    SGP_NRIC="Singapore NRIC"
    SGP_FIN="Singapore FIN"
    SGP_ASGD="Singapore ASGD"
    SGP_ITR="Singapore ITR"
    SLV_NIT="El Salvador NIT"
    SWE_TAX_ID="Sweden Tax ID (Personnummer)"
    URY_RUT="Uruguay RUT"
    VEN_RIF="Venezuela RIF"
    NOT_SPECIFIED="Other Tax IDs"

class VisaType(ExtendedEnum):
    B2="USA Visa Category B-2"
    B1="USA Visa Category B-1"
    DACA="USA Visa Category DACA"
    E1="USA Visa Category E-1"
    E2="USA Visa Category E-2"
    E3="USA Visa Category E-3"
    F1="USA Visa Category F-1"
    G4="USA Visa Category G-4"
    H1B="USA Visa Category H-1B"
    J1="USA Visa Category J-1"
    L1="USA Visa Category L-1"
    Other="Any other USA Visa Category"
    O1="USA Visa Category O-1"
    TN1="USA Visa Category TN-1"

class Fixture(ExtendedEnum):
    SUBMITTED="/fixtures/status=SUBMITTED/fixtures/"
    ACTION_REQUIRED="/fixtures/status=ACTION_REQUIRED/fixtures/"
    APPROVAL_PENDING="/fixtures/status=APPROVAL_PENDING/fixtures/"
    APPROVED="/fixtures/status=APPROVED/fixtures/"
    REJECTED="/fixtures/status=REJECTED/fixtures/"
    ACTIVE="/fixtures/status=ACTIVE/fixtures/"
    DISABLED="/fixtures/status=DISABLED/fixtures/"
    ACCOUNT_CLOSED="/fixtures/status=ACCOUNT_CLOSED/fixtures/"


class RegiesterRepsonse(ExtendedEnum):
    ACCOUNT_EXIST = "Account with this email already exists"
    ACCOUNT_CREATED = "Account created successfully"
    EMAIL_NOT_VALID = "email is not a valid email address"
    PASSWORD_TO_COMMON = "Password is to common"
    PASSWORD_SIMILIAR = "Password is similiar to username/email"

class AuthorizationEnum(ExtendedEnum):
    PERMISSIONS_ERROR ='User is not Registered or has permission'


class ApiErrorMessage(ExtendedEnum):
    ERROR_429 = "Too many request"
    ERROR_400 = "Bad request / invaid payload"
