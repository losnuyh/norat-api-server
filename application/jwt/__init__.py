from .token_manager import JwtTokenManager

jwt_token_manager = JwtTokenManager(
    private_key="""-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEILWhIooU6PsWtjat3n1wIx7Alru9PupjDpKmwQbxhOYE
-----END PRIVATE KEY-----""",
)
