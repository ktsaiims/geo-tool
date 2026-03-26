# Geography Tool

A command-line tool that looks up geographic information for a given ZIP code using the USPS and Google Maps APIs.

# Features

- Look up the **city and state** for a ZIP code (via USPS API)
- Look up the **latitude and longitude** for a ZIP code (via Google Maps Geocoding API)

# Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (recommended)

# Setup

## 1. Install dependencies

Use `uv`:
```
uv sync
```

Alternatively, use `pip`:
```
pip install -r requirements.txt
```

## 2. Configure environment variables

Create a `.env` file in the project root with the following keys:

```
# Google Maps API key (required for --coordinates)
GOOGLE_API_KEY=your_google_api_key_here

# USPS credentials (required for --citystate)
USPS_CLIENT_ID=your_usps_client_id_here
USPS_CLIENT_SECRET=your_usps_client_secret_here

# Optional: if you already have a USPS access token, you can provide it directly and skip the token exchange step
USPS_ACCESS_TOKEN=your_usps_access_token_here
```

> **Note:** USPS access tokens are fetched and cached automatically in `./usps_token.json` the first time you run the tool with valid client credentials.

# Usage

```
python main.py <zipcode> --citystate
python main.py <zipcode> --coordinates
```

The `--citystate` and `--coordinates` flags are mutually exclusive - you must provide exactly one.

## Examples

```
python main.py 90210 --citystate
# city: BEVERLY HILLS, state: CA
```

```
python main.py 90210 --coordinates
# latitude: 34.0901, longitude: -118.4065
```

# Project Structure

```
geography-tool/
├── main.py                  # Entry point and CLI argument parsing
├── configs.py               # Logging level and timestamp config
├── src/
│   ├── paths.py             # Directory path definitions
│   ├── routes.py            # Core logic for each CLI command
│   ├── utils.py             # Logging and directory setup
│   ├── authentications/
│   │   ├── google_auth.py   # Validates Google API key from .env
│   │   └── usps_auth.py     # Fetches and caches USPS access token
│   └── classes/
│       ├── GeographyResult.py        # Result dataclass with validation
│       └── api/
│           ├── google_client.py      # Google Maps Geocoding API client
│           └── usps_client.py        # USPS Addresses API client
├── data/                    # Reserved for data output
└── logs/                    # Auto-generated log files (one per run)
```

# API References

## Google

See the official Google Geocoding API [documentation](https://developers.google.com/maps/documentation/geocoding/overview).

## USPS

### Access Token

Base URL: `https://apis.usps.com/oauth2/v3`

An access token is needed to call API endpoints. For more details, see the official USPS [documentation](https://developers.usps.com/Oauth).

**Prerequisites**

- Client ID
- Client Secret

**Token Request**

Endpoint: `POST /token`

Send a POST request to the `/token` endpoint with the following parameters:

```
grant_type=client_credentials
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
```

Curl example:

```bash
curl -X POST https://apis.usps.com/oauth2/v3/token -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=client_credentials" -d "client_id=YOUR_CLIENT_ID" -d "client_secret=YOUR_CLIENT_SECRET"
```

**Token Response**

The endpoint returns a JSON response containing:

- `access_token`: Your authentication token (in JWT format)
- `token_type`: Bearer
- `expires_in`: Token expiration time in seconds
- `refresh_token` (optional): Used to obtain a new access token without re-authenticating

**Response Example**

```json
{
    "access_token": "...",
    "token_type": "Bearer",
    "issued_at": 1770832540667,
    "expires_in": 28799,
    "status": "approved",
    "scope": "domestic-prices  oauth2-oidc addresses international-prices openid  usps:MIDs shipments tracking  usps:payment_methods service-standards-files service-standards locations international-service-standard",
    "issuer": "https://keyc.usps.com/realms/USPS",
    "client_id": "...",
    "application_name": "IMS Shipping Prices",
    "api_products": "[Public Access I]",
    "public_key": "..."
}
```

**Expiration**

Access tokens are valid for eight hours after issuance, while refresh tokens are valid for seven days. Check your token's `expires_in`.

### Addresses

Base URL: `https://apis.usps.com/addresses/v3` 

The Addresses API validates and corrects address information to improve package delivery service and pricing. This suite of APIs provides different utilities for addressing components, including:

- Address Standardization
- City/State Lookup
- ZIP Code Lookup

For more details, see the official USPS [documentation](https://developers.usps.com/addressesv3).

**Address Standardization**

Endpoint: `GET /address`

Validates and standardizes USPS domestic addresses, city and state names, and ZIP Code in accordance with USPS addressing standards, including ZIP + 4.

<details>

<summary>Examples</summary>

| Parameter Name | Type | Required | Description |
|------|------|----------|-------------|
| **firm** | string | No | Firm/business corresponding to the address. Max length: 50 |
| **streetAddress** | string | Yes | The number of a building along with the name of the road or street on which it is located . |
| **secondaryAddress** | string | No | The secondary unit designator, such as apartment (APT) or suite (STE) number, defining the exact location of the address within a building . Max length: 50 |
| **city** | string | No | The city name of the address . |
| **state** | string | Yes | The two-character state code of the address. Valid values: AA, AE, AL, AK, AP, AS, AZ, AR, CA, CO, CT, DE, DC, FM, FL, GA, GU, HI, ID, IL, IN, IA, KS, KY, LA, ME, MH, MD, MA, MI, MN, MS, MO, MP, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PW, PA, PR, RI, SC, SD, TN, TX, UT, VT, VI, VA, WA, WV, WI, WY |
| **urbanization** | string | No | The urbanization code relevant only for Puerto Rico addresses. |
| **ZIPCode** | string | No | The 5-digit ZIP code. Pattern: `^\d{5}$` |
| **ZIPPlus4** | string | No | The 4-digit component of the ZIP+4 code. Using the correct ZIP+4 reduces the number of times your mail is handled and can decrease the chance of a misdelivery or error. Pattern: `^\d{4}$` |

Example Request:

```
GET /address?streetAddress=1600+Pennsylvania+Ave&city=Washington&state=DC
```

</details>

**City/State Lookup**

Endpoint: `GET /city-state`

Provides valid cities and states for a provided ZIP Code.

<details>

<summary>Examples</summary>

| Parameter Name | Type | Required | Description |
|------|------|----------|-------------|
| **ZIPCode** | string | Yes | The 5-digit ZIP code. Pattern: `^\d{5}$` |

Example Request:

```
GET /city-state?ZIPCode=10001
```

</details>

**ZIP Code Lookup**

Endpoint: `GET /zipcode`

Finds valid ZIP Code(s) for a Street, City, and State.

<details>

<summary>Examples</summary>

| Parameter Name | Type | Required | Description |
|------|------|----------|-------------|
| **firm** | string | No | Firm/business corresponding to the address. Max length: 50 |
| **streetAddress** | string | Yes | The number of a building along with the name of the road or street on which it is located [2]. |
| **secondaryAddress** | string | No | The secondary unit designator, such as apartment (APT) or suite (STE) number, defining the exact location of the address within a building [2]. |
| **city** | string | Yes | The city name of the address [2]. |
| **state** | string | Yes | The two-character state code of the address. Valid values: AA, AE, AL, AK, AP, AS, AZ, AR, CA, CO, CT, DE, DC, FM, FL, GA, GU, HI, ID, IL, IN, IA, KS, KY, LA, ME, MH, MD, MA, MI, MN, MS, MO, MP, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PW, PA, PR, RI, SC, SD, TN, TX, UT, VT, VI, VA, WA, WV, WI, WY |
| **ZIPCode** | string | No | The 5-digit ZIP code. Pattern: `^\d{5}$` |
| **ZIPPlus4** | string | No | The 4-digit component of the ZIP+4 code. Using the correct ZIP+4 reduces the number of times your mail is handled and can decrease the chance of a misdelivery or error. Pattern: `^\d{4}$` |

Example Request:

```
GET /zipcode?streetAddress=1600+Pennsylvania+Ave&city=Washington&state=DC
```

</details>
