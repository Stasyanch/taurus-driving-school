<?php
use PHPUnit\Framework\TestCase;

class ValidationTest extends TestCase {
    public function testValidEmail() {
        $email = "student@taurus.kiev.ua";
        $this->assertTrue((bool)filter_var($email, FILTER_VALIDATE_EMAIL));
    }

    public function testPhoneLength() {
        $phone = "+380991234567";
        $this->assertGreaterThanOrEqual(10, strlen($phone));
    }

    public function testAgeEligibility() {
        $age = 18;
        $isEligible = $age >= 18;
        $this->assertTrue($isEligible);
    }
}
