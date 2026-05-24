#!/usr/bin/env ruby
class CaesarCipher
  def initialize(shift)
    @shift = shift
  end

  def encrypt(message)
    cipher(message, @shift)
  end

  def decrypt(message)
    cipher(message, -@shift)
  end

  private

  def cipher(message, shift_value)
    result = ""

    message.each_char do |char|
      if char.match?(/[a-z]/)
        base = 97
        shifted_char = ((char.ord - base + shift_value) % 26 + base).chr
        result += shifted_char
      elsif char.match?(/[A-Z]/)
        base = 65
        shifted_char = ((char.ord - base + shift_value) % 26 + base).chr
        result += shifted_char
      else
        result += char
      end
    end

    result
  end
end
