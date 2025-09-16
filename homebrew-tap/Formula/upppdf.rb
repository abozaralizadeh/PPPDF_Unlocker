class Upppdf < Formula
  desc "Unlock password protected PDF files using multiple methods"
  homepage "https://github.com/abozaralizadeh/UPPPDF"
  url "https://github.com/abozaralizadeh/UPPPDF/archive/refs/tags/v1.0.5.tar.gz"
  sha256 "ea2a33cda49c0abf595d72350a16b5f8a28ad36df6364caeac6831392e3bd08f"
  license "MIT"

  head "https://github.com/abozaralizadeh/UPPPDF.git", branch: "master"

  depends_on "python@3.11"

  def install
    system "python3", "-m", "pip", "install", *std_pip_args, "."
  end

  test do
    system "#{bin}/upppdf", "--help"
  end
end