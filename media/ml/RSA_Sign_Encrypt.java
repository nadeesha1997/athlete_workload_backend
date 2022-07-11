package Cryptography;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.security.spec.EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

public class RSA_Sign_Encrypt {

	public static void main(String[] args) throws NoSuchAlgorithmException, FileNotFoundException, IOException, NoSuchPaddingException, InvalidKeyException, IllegalBlockSizeException, BadPaddingException {
		
		KeyPairGenerator key_gen = KeyPairGenerator.getInstance("RSA");
		key_gen.initialize(2048);
		KeyPair alice_key_pair = key_gen.generateKeyPair();

		PrivateKey alice_pvt_key = alice_key_pair.getPrivate();
		PublicKey alice_pub_key = alice_key_pair.getPublic();
		
		KeyPair bob_key_pair = key_gen.generateKeyPair();

		PrivateKey bob_pvt_key = bob_key_pair.getPrivate();
		PublicKey bob_pub_key = bob_key_pair.getPublic();

		//System.out.println("Alice Private Key : " + new String(alice_pvt_key.getEncoded()));
		//System.out.println("Alice Public Key : " + new String(alice_pub_key.getEncoded()));
		
		//System.out.println("Bob Private Key : " + new String(bob_pvt_key.getEncoded()));
		//System.out.println("Bob Public Key : " + new String(bob_pub_key.getEncoded()));
		
		
		String secretMessage = "Sample secret message";
		System.out.println("Plain Text : " + secretMessage);
		
		Cipher cipher = Cipher.getInstance("RSA/ECB/NoPadding");
		cipher.init(Cipher.ENCRYPT_MODE, alice_pvt_key);
		
		byte[] secretMessageBytes = secretMessage.getBytes(StandardCharsets.UTF_8);
		byte[] signed_text = cipher.doFinal(secretMessageBytes);
		
		System.out.println("Signed Text : " + new String(signed_text));
		System.out.println("Signed Text : " + signed_text.length);
		
		cipher.init(Cipher.ENCRYPT_MODE, bob_pub_key);
		byte[] enc_signed_text = cipher.doFinal(signed_text);
		
		String encodedMessage = Base64.getEncoder().encodeToString(enc_signed_text);
		
		System.out.println("Encoded Encrypted Signed Cipher Text : " + encodedMessage);
		
		// Transmit
		
		cipher.init(Cipher.DECRYPT_MODE, bob_pvt_key);
		
		byte[] decryptedMessageBytes = cipher.doFinal(enc_signed_text);
		System.out.println("Decrypted Signed Cipher Text : " + new String(decryptedMessageBytes));
		
		cipher.init(Cipher.DECRYPT_MODE, alice_pub_key);
		
		byte[] dec_var_text = cipher.doFinal(decryptedMessageBytes);
		
		String decryptedMessage = new String(dec_var_text, StandardCharsets.UTF_8);
		
		System.out.println("Retrieved Plain Text : " + decryptedMessage.trim());

	}

}
