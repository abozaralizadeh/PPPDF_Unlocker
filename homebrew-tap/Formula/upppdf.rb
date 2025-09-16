class Upppdf < Formula
  desc "Unlock password protected PDF files using multiple methods"
  homepage "https://github.com/abozar/PDF_Unlocker"
  url "https://github.com/abozar/PDF_Unlocker/archive/refs/tags/v1.0.0.tar.gz"
  sha256 ""
  license "MIT"
  head "https://github.com/abozar/PDF_Unlocker.git", branch: "master"

  depends_on "python@3.11"

  def install
    system "python3.11", "-m", "pip", "install", *std_pip_args, "."
  end

  test do
    system "#{bin}/upppdf", "--help"
  end
end
