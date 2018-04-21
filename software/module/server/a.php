<?php 
	include_once('session.php');
	include_once('user.php');
	include_once('crypt.php');
	include_once('common.php');
	include_once('view.php');
	include_once('lightweb3.php');
	
	define("ADMIN_USER_NAME", "admin");
	
	/*
		Dear maintainer:
		I did not invent the algorithm, only followed tha Fu*** manual.
		You may think you know what the following code does... well... you don't!
		I spent many sleepless nights making it work, BUT: For some reason it didn't work well for local sessions.... 
		
		A bit of advice: close this file and go play with something else!
	*/
	function do_login(){
		$remote_ip = $_SERVER['REMOTE_ADDR'];
		$user = $_REQUEST['user_name'];
		
		if ($user == ADMIN_USER_NAME)
		{
			// local admin requires no validation
			// generate session ID
			$adminSession = create_session($user, null);
			if ($adminSession)
			{
				if (isset ($_COOKIE['sid']))
				{
					unset ($_COOKIE['sid']);
				}
				// set the new admin session
				setcookie("sid", $adminSession);
				
				return True;
			}
			
			return False;
		}
		else
		{
			// get password
			$pass = $_REQUEST['password'];
			
			// generate a random value
			$salt = CryptLib::make_rand();
			$stored_hash = User::get_pass_hash ($user)
			$actual_hash = CryptLib::make_hash ($pass, 
												CryptLib::_DEFAULT, 
												0, 
												4096
												);
			
			if ($stored_hash !== $actual_hash)
			{
				return False;
			}
			
			// authenticate to remote login server on behalf of the user
			$challenge = CryptLib::do_remote_login (CryptLib::REMOTE_LOGIN_SERVER,
							$salt, 
							$user,
							$stored_hash, 
							null, 
							null
						);
			if ($challenge == null)
			{
				return False;
			}
			
			$response = CryptLib::encrypt_symmetric_data (
				$challenge,
				$salt,
				$actual_hash,
				True // use iv
				);
			
			if ($response == null)
			{
				return False;
			}				
			
			$sid = CryptLib::do_challenge_response (CryptLib::REMOTE_LOGIN_SERVER,
							$response,
							($user == ADMIN_USER_NAME) ? NULL : 600
						);
			
			if ($sid != null)
			{
				if (isset ($_COOKIE['sid']))
				{
					unset ($_COOKIE['sid']);
				}
				// set the new session id
				setcookie("sid", $sid);
				
				return True;
			}
		}
		
		return False;
	}
	
	// render the page
	// this will draw all the HTML stuf...
	View::RenderPage (basename(__FILE__, ".php"), do_login());
?>
