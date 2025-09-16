class Upppdf < Formula
  desc "Unlock password protected PDF files using multiple methods"
  homepage "https://github.com/abozaralizadeh/UPPPDF"
  url "https://github.com/abozaralizadeh/UPPPDF/archive/refs/tags/v1.0.9.tar.gz"
  sha256 "6042e6a22b001050b705e56aec93112e5ae7cb2ebfd5db56615796dd69a41514"
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